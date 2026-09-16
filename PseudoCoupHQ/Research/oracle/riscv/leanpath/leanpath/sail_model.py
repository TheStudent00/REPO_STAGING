"""SailModel -- the ratified Sail RISC-V model as the one source of every
definition, read by the sail compiler's Lean backend, never by a person.

Plan leaf: lean_proof_path.sail_model, with methods definitions, key_of,
strip, and the work node emit_lane (a tower lane: lanes_lp1/lp1_l7b_*.sh).

The one place Python reads the emitted Lean TEXT, and only to LIST: the
`execute` clauses, the `instruction` constructors and their operand
tuples, the `assembly_forwards` clause of each constructor (the mnemonic
as the model spells it) and the `*_mnemonic_forwards` maps it calls.
Nothing here rewrites a definition; `strip` (the pure expression Lean
holds after `simp` unfolds the reads and the write) runs the model's own
`execute` on the definition's instance in Lean and prints the form
(the third launch's build passes: log 277).

The harness side (third launch): `harness_names` LISTS every def and
value-abbrev of the emitted tree (the unfold set `leanpath_model`),
`axioms` LISTS the support library's `SailM Unit` axioms (the
hypotheses every theorem carries), `registers` LISTS the `Register`
inductive's constructors, `base` runs the model's own init and reset
in Lean and records the state, `instances` builds one Lean instruction
term per key from the model's own dispatch, maps and inductive.
"""

import itertools
import os
import re

AWAITS_BUILT_MODEL = "AWAITS_BUILT_MODEL"


class SailModel:
    """attributes: commit (the cache key), modules (leaf module names),
    lean_tree (the emitted Lean, keyed by commit)."""

    def __init__(self, commit, modules, lean_tree):
        self.commit = commit
        self.modules = modules
        self.lean_tree = lean_tree

    # ---------------------------------------------------------------- #
    # definitions(model) -> list[ArchOpcode]
    # ---------------------------------------------------------------- #
    @staticmethod
    def definitions(lean_tree, model_source):
        """definitions(model) -> the list of arch-opcodes, one per execute
        clause of the selected modules.

        Steps, in order:
          1. read the Lean tree for this commit (the cache; a miss means
             the emit lane runs first -- not done here, it is a lane)
          2. for every `def execute_<NAME>` in the tree build the
             ArchOpcode: keys from `key_of`, definition from `strip`
          3. return the list; a clause `strip` refuses is a row with the
             refusal named, never dropped

        With no built model, every row's `definition` is the refusal
        AWAITS_BUILT_MODEL and `source_clause` is the raw emitted text.
        Returns a dict with the counts "of N" and the rows, ready to be
        written as json and walked by the spelling guard.
        """
        from .arch_opcode import ArchOpcode
        text = SailModel._read_tree(lean_tree)
        clauses = SailModel._execute_clauses(lean_tree)
        ext_of = SailModel._extension_of_clause(model_source)
        ctor_tuple = SailModel._instruction_constructors(text)
        maps = SailModel._mnemonic_maps(text)
        asm = SailModel._assembly_clauses(text)
        keys = []
        rows = []
        for name, fn, clause_text in clauses:
            ext = ext_of.get(name, "unresolved")
            width = SailModel._width_of_clause(clause_text)
            form = SailModel._operand_form(ctor_tuple.get(name, ""))
            mnems = SailModel.key_of(name, asm, maps)
            row = {
                "clause": "execute_%s" % name,
                "file": fn,
                "extension": ext,
                "operand_form": form,
                "width": width,
                "mnem_count": len(mnems),      # each mnemonic is a key row below, in the exempt field `mnem`
                "definition": AWAITS_BUILT_MODEL,
                "source_clause_lines": clause_text.count("\n") + 1,
            }
            rows.append(row)
            for m in mnems:
                keys.append(ArchOpcode(
                    key={"mnem": m, "operand_form": form, "width": width},
                    definition=AWAITS_BUILT_MODEL,
                    source_clause="execute_%s" % name).as_row())
        by_ext = {}
        for r in rows:
            by_ext.setdefault(r["extension"], []).append(r["clause"])
        return {
            "clause_count": len(rows),
            "clauses_by_extension": {e: sorted(v) for e, v in by_ext.items()},
            "clauses": rows,
            "key_count": len(keys),
            "keys": keys,
        }

    # ---------------------------------------------------------------- #
    # key_of(clause) -> key
    # ---------------------------------------------------------------- #
    @staticmethod
    def key_of(ctor, asm, maps):
        """key_of(clause) -> the mnemonics the model's own assembly clause
        spells for this constructor (the mnemonic part of the key; the
        operand form and width are read beside it by `definitions`).

        Steps, in order:
          1. take the constructor's `assembly_forwards` clause as Lean
             wrote it: a `String.append` chain
          2. read the parts BEFORE the first `spc_forwards ()`: a string
             literal, or a call of a `*_forwards` map (`maybe_u`, `w`,
             the op-enum's mnemonic map)
          3. expand each map call to the strings its clauses give, and
             take every combination in order (the width suffix rule is
             the clause's own)
          4. return the list; nothing else about the instruction is read
        """
        chain = asm.get(ctor)
        if chain is None:
            return []
        parts = []
        for kind, val in chain:
            if kind == "lit":
                parts.append([val])
            elif kind == "call":
                if val in maps:
                    parts.append(sorted(set(maps[val].values())))
                else:
                    return []      # a part this reader does not know: no key, not a guess
        out = []
        for combo in itertools.product(*parts):
            out.append("".join(combo))
        return sorted(set(out))

    # ---------------------------------------------------------------- #
    # strip(execute_clause) -> LeanExpr
    # ---------------------------------------------------------------- #
    @staticmethod
    def strip(instance, project, workdir, name, hyps):
        """strip(execute_clause) -> the pure expression the answering
        register holds after Sail's own `execute`, over the read registers
        left unknown: the model's `execute` applied to the clause's
        INSTANCE (the constructor with the argument registers x10, x11 and
        the answer register x10; a selector from the model's own mnemonic
        map; an immediate as an unknown), run on the base state in Lean
        and unfolded by `simp`; the form is printed by the harness's own
        tactic, LITERAL, and the RUN is what later theorems are stated
        over. A clause whose run does not retire, or leaves a residual
        the unfolding does not reach, is a refusal with the construct
        named."""
        from .arch_unit import ArchUnit
        run = "(execute (%s))" % instance["term"]
        return ArchUnit.form_of(run, project, workdir, name, hyps, unknowns=instance.get("unknowns", {}))

    # ---------------------------------------------------------------- #
    # the harness listings (text only: names, never a definition)
    # ---------------------------------------------------------------- #
    @staticmethod
    def import_closure(cache_root):
        """the emitted modules `import LeanIM` reaches: LeanIM.lean's
        imports followed transitively (the emit writes modules nothing
        imports; they are not in the built library and their names do
        not exist)."""
        seen = []
        todo = ["LeanIM"]
        while todo:
            mod = todo.pop()
            if mod in seen:
                continue
            seen.append(mod)
            path = os.path.join(cache_root, mod.replace(".", os.sep) + ".lean")
            if not os.path.exists(path):
                continue
            for line in open(path, errors="replace"):
                m = re.match(r'^import (LeanIM(?:\.[A-Za-z0-9_]+)?)\s*$', line)
                if m:
                    todo.append(m.group(1))
        return seen

    @staticmethod
    def harness_names(cache_root):
        """every `def`/`noncomputable def` and every value-typed `abbrev`
        (`: Int :=`, `: Nat :=`, `: Bool :=`) of the emitted modules in the
        import closure of LeanIM.lean, with its namespace, in import
        order: the unfold set of the harness. Names of instances and of
        the executable's `main` are left out (an instance is not
        unfolded; `main` is IO)."""
        out = []
        for mod in SailModel.import_closure(cache_root):
            path = os.path.join(cache_root, mod.replace(".", os.sep) + ".lean")
            if os.path.exists(path):
                out.extend(SailModel.harness_names_of_file(path))
        seen = set()
        uniq = []
        for n in out:
            if n not in seen:
                seen.add(n)
                uniq.append(n)
        return uniq

    @staticmethod
    def harness_names_of_file(path):
        text = open(path, errors="replace").read()
        out = []
        ns = []
        for line in text.splitlines():
            m = re.match(r'^namespace ([A-Za-z0-9_.]+)', line)
            if m:
                ns.append(m.group(1))
                continue
            m = re.match(r'^end ([A-Za-z0-9_.]+)', line)
            if m and ns and ns[-1] == m.group(1):
                ns.pop()
                continue
            if m and ns and ".".join(ns) == m.group(1):
                ns[:] = []
                continue
            m = re.match(r'^(?:noncomputable )?def ([A-Za-z0-9_]+)\b', line)
            if not m:
                m = re.match(r'^abbrev ([A-Za-z0-9_]+)\s*(?:\([^)]*\)\s*)*:\s*(?:Int|Nat|Bool)\s*:=', line)
            if m:
                nm = m.group(1)
                if nm in ("main", "instance") or nm.startswith("inst"):
                    continue
                out.append(".".join(ns + [nm]))
        return out

    @staticmethod
    def signature_of(lean_tree, name):
        """the `def <name> ...` line of the emitted tree, LITERAL, or None."""
        for fn in sorted(os.listdir(lean_tree)):
            if not fn.endswith(".lean"):
                continue
            for line in open(os.path.join(lean_tree, fn), errors="replace"):
                if re.match(r'^(?:noncomputable )?def %s\b' % re.escape(name), line):
                    return line.rstrip()
        return None

    @staticmethod
    def axioms(lean_tree):
        """the axioms of the model's handwritten support (RiscvExtras.lean)
        whose type ends in `SailM Unit`: name and its arrow type, LITERAL.
        Every theorem assumes each leaves the state as it is."""
        out = []
        for fn in sorted(os.listdir(lean_tree)):
            if not fn.endswith(".lean"):
                continue
            for line in open(os.path.join(lean_tree, fn), errors="replace"):
                m = re.match(r'^axiom ([A-Za-z0-9_]+)\s*(\{[^}]*\}\s*)?:\s*(.*)$', line.rstrip())
                if m and m.group(3).strip().endswith("SailM Unit"):
                    out.append({"name": m.group(1), "type": m.group(3).strip(), "file": fn, "line": line.rstrip()})
        return out

    @staticmethod
    def axiom_hyps(axioms):
        """the hypothesis text: one per axiom, `(h_<name> : ∀ x s,
        <name> x s = EStateM.Result.ok () s)` (the arity from the type's
        arrows)."""
        parts = []
        for ax in axioms:
            arrows = ax["type"].count("→")
            xs = " ".join("x%d" % i for i in range(arrows))
            parts.append("(h_%s : ∀ %s (s : Leanpath.St), (%s %s) s = EStateM.Result.ok () s)"
                         % (ax["name"], (xs + " ") if xs else "", ax["name"], xs))
        return " ".join(parts), ["h_%s" % ax["name"] for ax in axioms]

    @staticmethod
    def registers(lean_tree):
        """the constructors of the emitted `inductive Register`, in order."""
        text = SailModel._read_tree(lean_tree)
        m = re.search(r'inductive Register : Type where\n(.*?)\n  deriving', text, re.S)
        if not m:
            return []
        return re.findall(r'^  \| ([A-Za-z0-9_]+)', m.group(1), re.M)

    @staticmethod
    def instances(lean_tree):
        """one Lean instruction term per key of `definitions`, from the
        model's own text and nothing else:
          - the constructor and its parameter NAMES from the `execute`
            dispatch (`| .RTYPE (rs2, rs1, rd, op) => ...`)
          - each parameter's TYPE from the `instruction` inductive's tuple
          - a parameter typed `regidx` named rs1/rs2 gets the argument
            registers x10/x11 in that order and one named rd the answer
            register x10 (the model's own parameter names)
          - a parameter whose type is the argument type of a mnemonic map
            the assembly clause calls gets that map's PATTERN for the key
            (`.ADD`, `{ result_part := .High, ... }`, `true`)
          - a parameter typed `BitVec n` (an immediate) becomes an unknown
            `imm_k : BitVec n` the theorem quantifies over
          - any other parameter is a refusal for that key, named
        Returns {key -> {"term", "unknowns", "ctor", "refusal"}}."""
        text = SailModel._read_tree(lean_tree)
        ctor_tuple = SailModel._instruction_constructors(text)
        maps = SailModel._mnemonic_maps(text)
        map_arg = SailModel._map_arg_types(text)
        asm = SailModel._assembly_clauses(text)
        arms = SailModel._execute_arms(text)
        out = {}
        for ctor, params in arms.items():
            types = [t.strip() for t in ctor_tuple.get(ctor, "").split("×")] if ctor in ctor_tuple else []
            if len(types) != len(params):
                continue
            chain = asm.get(ctor)
            if chain is None:
                continue
            combos = SailModel._key_combos(chain, maps)
            for mnem, choice in combos:
                args = []
                unknowns = {}
                refusal = None
                k = 0
                for pname, ptype in zip(params, types):
                    if ptype == "regidx":
                        if pname == "rs1":
                            args.append("Regidx 10#5")
                        elif pname == "rs2":
                            args.append("Regidx 11#5")
                        elif pname == "rd":
                            args.append("Regidx 10#5")
                        else:
                            refusal = "regidx parameter %s is neither rs1, rs2 nor rd" % pname
                    elif ptype.startswith("BitVec"):
                        w = ptype.replace("BitVec", "").strip(" ()")
                        nm = "imm%d" % k
                        k += 1
                        args.append(nm)
                        unknowns[nm] = "BitVec %s" % w
                    else:
                        pat = None
                        for mp, p in choice.items():
                            if map_arg.get(mp) == ptype:
                                pat = p
                        if pat is None:
                            refusal = "parameter %s : %s has no selector in the assembly clause" % (pname, ptype)
                        else:
                            args.append(pat)
                term = "%s (%s)" % (ctor, ", ".join(args)) if len(args) > 1 else "%s %s" % (ctor, args[0] if args else "()")
                out[(mnem, ctor)] = {"term": term, "unknowns": unknowns, "ctor": ctor, "refusal": refusal, "params": params, "types": types}
        return out

    @staticmethod
    def _execute_arms(text):
        m = re.search(r'^def execute \(merge_var : instruction\) : SailM ExecutionResult := do\n  match merge_var with\n(.*?)(?=\n\n)', text, re.M | re.S)
        out = {}
        if not m:
            return out
        for line in m.group(1).splitlines():
            a = re.match(r'  \| \.([A-Za-z0-9_]+) \(([^)]*)\) =>', line)
            if a:
                out[a.group(1)] = [p.strip() for p in a.group(2).split(",")]
                continue
            a = re.match(r'  \| \.([A-Za-z0-9_]+) ([A-Za-z0-9_]+) =>', line)
            if a:
                out[a.group(1)] = [a.group(2)]
        return out

    @staticmethod
    def _map_arg_types(text):
        out = {}
        for m in re.finditer(r'^def ([A-Za-z0-9_]+_forwards) \(arg_ : ([^)]*)\) : (?:SailM )?String', text, re.M):
            out[m.group(1)] = m.group(2).strip()
        return out

    @staticmethod
    def _key_combos(chain, maps):
        """[(mnemonic, {map -> pattern})] for the parts before the first
        spc_forwards (): every combination of the maps' clauses."""
        parts = []
        for kind, val in chain:
            if kind == "lit":
                parts.append([(val, None, None)])
            elif kind == "call":
                if val not in maps:
                    return []
                parts.append([(s, val, p) for p, s in sorted(maps[val].items())])
        out = []
        for combo in itertools.product(*parts):
            mnem = "".join(c[0] for c in combo)
            choice = {c[1]: c[2] for c in combo if c[1] is not None}
            out.append((mnem, choice))
        seen = {}
        for mnem, choice in out:
            seen.setdefault(mnem, choice)
        return sorted(seen.items())

    # ---------------------------------------------------------------- #
    # the readers (text listing only)
    # ---------------------------------------------------------------- #
    @staticmethod
    def _read_tree(lean_tree):
        parts = []
        for fn in sorted(os.listdir(lean_tree)):
            if fn.endswith(".lean"):
                parts.append(open(os.path.join(lean_tree, fn), errors="replace").read())
        return "\n".join(parts)

    @staticmethod
    def _execute_clauses(lean_tree):
        out = []
        for fn in sorted(os.listdir(lean_tree)):
            if not fn.endswith(".lean"):
                continue
            src = open(os.path.join(lean_tree, fn), errors="replace").read()
            for m in re.finditer(r'^(?:noncomputable )?def execute_([A-Za-z0-9_]+) .*?$', src, re.M):
                start = m.start()
                end = src.find("\n\n", start)
                body = src[start:end if end > 0 else len(src)]
                out.append((m.group(1), fn, body))
        return out

    @staticmethod
    def _extension_of_clause(model_source):
        src_of = {}
        for root, _dirs, files in os.walk(model_source):
            for fn in files:
                if not fn.endswith(".sail"):
                    continue
                path = os.path.join(root, fn)
                try:
                    text = open(path, errors="replace").read()
                except OSError:
                    continue
                for m in re.finditer(r'function clause execute\s+([A-Za-z0-9_]+)\b', text):
                    src_of.setdefault(m.group(1), path)
        out = {}
        for name, path in src_of.items():
            parts = path.split(os.sep)
            if "extensions" in parts:
                out[name] = parts[parts.index("extensions") + 1]
            elif "postlude" in parts:
                out[name] = "postlude"
            else:
                out[name] = parts[-2]
        return out

    @staticmethod
    def _instruction_constructors(text):
        m = re.search(r'inductive instruction where\n(.*?)\n  deriving', text, re.S)
        out = {}
        if not m:
            return out
        for cn, tup in re.findall(r'\| ([A-Za-z0-9_]+) \(_ : \(?([^\n]*?)\)?\)(?:\n|$)', m.group(1)):
            out[cn] = tup.replace("(", "").replace(")", "").strip()
        return out

    @staticmethod
    def _operand_form(tup):
        kinds = []
        for t in [x.strip() for x in tup.split("×")]:
            if t == "regidx":
                kinds.append("reg")
            elif t.startswith("BitVec"):
                kinds.append("imm" + t.replace("BitVec", "").strip())
            # an op-enum, Bool or width selector is the clause's internal
            # selector, not an operand kind: not part of the form
        return " ".join(kinds)

    @staticmethod
    def _width_of_clause(clause_text):
        """64 (xlen as instantiated) unless the clause writes a 32-bit
        value sign-extended into the register, its own narrower width."""
        if re.search(r'wX_bits \w+ \(sign_extend \(m := 64\)', clause_text) and \
           re.search(r'extractLsb [^\n]*? 31 0|BitVec 32\)|to_bits_truncate \(l := 32\)', clause_text):
            return 32
        return 64

    @staticmethod
    def _mnemonic_maps(text):
        """every `def <name>_forwards (arg_ : T) : String` (or SailM String)
        whose clauses map a pattern to a string literal."""
        maps = {}
        for m in re.finditer(r'^def ([A-Za-z0-9_]+_forwards) \(arg_ : [^)]*\) : (?:SailM )?String :=(?: do)?\n(.*?)(?=\n\n)', text, re.M | re.S):
            name, body = m.group(1), m.group(2)
            table = {}
            for pat, s in re.findall(r'\| (.+?) => \(?(?:pure )?"([^"]*)"\)?', body):
                table[pat.strip()] = s
            if table:
                maps[name] = table
        return maps

    @staticmethod
    def _assembly_clauses(text):
        """constructor -> the parts of its assembly string before the first
        spc_forwards (): [("lit", s) | ("call", map_name)]."""
        m = re.search(r'^def assembly_forwards \(arg_ : instruction\) : SailM String := do\n  match arg_ with\n(.*?)(?=\n\n)', text, re.M | re.S)
        out = {}
        if not m:
            return out
        body = m.group(1)
        pieces = re.split(r'\n  \| \.', body)
        for piece in pieces:
            piece = piece.lstrip("| .")
            cm = re.match(r'([A-Za-z0-9_]+)\b', piece)
            if not cm:
                continue
            ctor = cm.group(1)
            head = piece.split("spc_forwards ()")[0]
            parts = []
            for tok in re.finditer(r'"([^"]*)"|\(← \(([A-Za-z0-9_]+_forwards) [^)]*\)\)|\(([A-Za-z0-9_]+_forwards) [^)]*\)', head):
                if tok.group(1) is not None:
                    if tok.group(1) != "":
                        parts.append(("lit", tok.group(1)))
                else:
                    parts.append(("call", tok.group(2) or tok.group(3)))
            if parts:
                out[ctor] = parts
        return out
