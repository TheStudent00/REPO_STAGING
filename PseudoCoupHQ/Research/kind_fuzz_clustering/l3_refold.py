#!/usr/bin/env python3
"""l3_refold.py -- log 035: fold the log-034 lanes into the products the
twelve-language clustering reads, so `l3_answers12.py` needs no change.

Three folds, each with the phase's standing completeness gate, each
superseding a named file rather than editing one in place.

  1. answers_swift.json   <- raw/xr_swift_00.txt over the accepted set
     in swiftfull_accepts.json (the FULL-`swiftc` one).  The superseded
     product, swift's execution over the `-typecheck` accepted set, is
     kept as SUPERSEDED_answers_swift_typecheck.json.

     THE CHECK: the old product recorded 1,066 CODEGEN_REFUSE rows.
     The new one must record ZERO, because its accepted set was taken
     with the compiler that would have done the refusing.  A non-zero
     count means the matrix redo did not do its job (log 034 section
     2.3).

  2. answers_cpp.json     <- the standing ex_cpp_* rows PLUS the six
     word-spelled operations from raw/xw_cpp_00.txt.  Additive: no
     symbol-spelled row is touched, and that is asserted rather than
     assumed.

  3. behavior_ruby_C.json <- raw/rc_ruby2.txt
     behavior_php_C.json  <- raw/rc_php2.txt
     the runs taken with the repaired route-C driver (log 034 section
     3.2).  The pre-repair products are kept as
     SUPERSEDED_behavior_<lang>_C_preparen.json.

Typescript's `instanceof` is admitted by decision 43 and has an EMPTY
domain -- `vw_typescript_00` accepted 0 of 10,000 probes -- so it folds
to no leaf.  That is recorded in refold_index.json, not passed over.
"""
import json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)
import l3_exec as E                                       # noqa: E402
import l3_read as R                                       # noqa: E402
import l3_wordexec as X                                    # noqa: E402
from l3_exec_read import split_enc                         # noqa: E402
from progress import Progress                              # noqa: E402


def read_rows(prefix, lang):
    """{probe id -> rest} over raw/<prefix>_<lang>_*.txt, plus summaries."""
    seen, summaries = {}, []
    files = sorted(f for f in os.listdir(RAW)
                   if f.startswith("%s_%s_" % (prefix, lang))
                   and f.endswith(".txt"))
    for fn in files:
        lines = open(os.path.join(RAW, fn), errors="replace").read().splitlines()
        pg = Progress(len(lines), "%s:%s" % (prefix, fn), every=20000)
        for line in lines:
            pg.tick()
            if line.startswith("__SUMMARY__"):
                summaries.append(line.split("|")[1:]); continue
            if "|" not in line:
                continue
            pid, rest = line.split("|", 1)
            if pid.startswith("P"):
                seen[pid] = rest
        pg.close()
    return seen, summaries, files


def build_rows(lang, ids, seen, HS, OPS):
    """the self-describing row shape of l3_exec_read.fold."""
    rows = []
    n = dict(answer=0, raise_=0, death=0, cg=0, miss=0)
    for t in ids:
        pid = "P%d_%d_%d_%d_%d" % t
        i, j, x, y, k = t
        ha, hb = HS[i], HS[j]
        row = dict(id=pid, operation=OPS[k],
                   lhs=dict(form=ha["form"], holder=ha["rep"],
                            value=ha["values"][x][0]),
                   rhs=dict(form=hb["form"], holder=hb["rep"],
                            value=hb["values"][y][0]))
        rest = seen.get(pid)
        if rest is None:
            row["outcome"] = "MISSING"; n["miss"] += 1
        elif rest.startswith("-|RAISE:"):
            row["outcome"] = "raise"; row["raise"] = rest[8:]; n["raise_"] += 1
        elif rest.startswith("-|DEATH:"):
            row["outcome"] = "death"; row["death"] = rest[8:]; n["death"] += 1
        elif rest.startswith("-|CODEGEN_REFUSE:"):
            row["outcome"] = "codegen_refuse"
            row["codegen_refuse"] = rest[17:]; n["cg"] += 1
        elif rest.startswith("-|BUILDFAIL"):
            row["outcome"] = "buildfail"; n["miss"] += 1
        else:
            tn, payload = rest.split("|", 1)
            enc, pay = split_enc(payload)
            row["outcome"] = "answer"
            row["result"] = dict(type=tn, encoding=enc, payload=pay)
            n["answer"] += 1
        rows.append(row)
    return rows, n


def doc(lang, route, rows, n, summaries, files, OPS, HS, extra=None):
    complete = (n["miss"] == 0 and bool(summaries))
    d = dict(language=lang, route=route,
             grain="one accepted (operation, holder pair, value pair) probe",
             probes=len(rows), answers=n["answer"], raises=n["raise_"],
             deaths=n["death"], codegen_refuse=n["cg"], missing=n["miss"],
             lanes=len(files), lane_summaries=summaries,
             complete=complete, completeness="COMPLETE" if complete else
             "SHORT -- %d missing of %d; do not read as a measurement"
             % (n["miss"], len(rows)),
             operations=OPS,
             holders=[dict(i=m, form=h["form"], rep=h["rep"])
                      for m, h in enumerate(HS)],
             rows=rows)
    d.update(extra or {})
    if not complete:
        print("  !! %s SHORT: %s" % (lang, d["completeness"]))
    return d


# ------------------------------------------------------------ 1, swift
def refold_swift():
    print("\n== 1. swift execution redo, full-swiftc accepted set")
    # RE-RUNNABLE.  The kept copy, not the live file, is the source of
    # truth for "what was superseded", so a second run of this script
    # reports the same table as the first rather than diffing its own
    # output against itself.
    old_p = os.path.join(HERE, "answers_swift.json")
    keep = os.path.join(HERE, "SUPERSEDED_answers_swift_typecheck.json")
    if not os.path.exists(keep):
        shutil.copy(old_p, keep)
    old = json.load(open(keep))
    ids = sorted(tuple(int(z) for z in s[1:].split("_"))
                 for s in json.load(open(
                     os.path.join(HERE, "swiftfull_accepts.json"))))
    T = E.table("swift")
    seen, summaries, files = read_rows("xr", "swift")
    rows, n = build_rows("swift", ids, seen, T["holders"], T["ops"])
    d = doc("swift", "C execution over the FULL-swiftc accepted set",
            rows, n, summaries, files, T["ops"], T["holders"],
            extra=dict(
                accepted_from="swiftfull_accepts.json",
                supersedes="answers_swift.json over the swiftc -typecheck "
                           "accepted set, kept as "
                           "SUPERSEDED_answers_swift_typecheck.json",
                superseded_codegen_refuse=old["codegen_refuse"]))
    json.dump(d, open(os.path.join(HERE, "answers_swift.json"), "w"))
    print("| set | probes | answers | codegen refuse |")
    print("|---|---|---|---|")
    print("| -typecheck accepts (superseded) | %d | %d | %d |"
          % (old["probes"], old["answers"], old["codegen_refuse"]))
    print("| full swiftc accepts | %d | %d | %d |"
          % (d["probes"], d["answers"], d["codegen_refuse"]))
    if d["codegen_refuse"] == 0:
        print("CHECK PASSES: zero codegen refusals, the matrix redo did "
              "its job")
    else:
        print("!! CHECK FAILS: %d codegen refusals remain"
              % d["codegen_refuse"])
    return d


# -------------------------------------------------------------- 2, cpp
def refold_cpp():
    print("\n== 2. cpp, the six word-spelled operations, additive")
    # RE-RUNNABLE, same rule as the swift fold: the symbols-only copy is
    # the base every run merges into, so running twice gives the same
    # file rather than folding the word operations in twice.
    p = os.path.join(HERE, "answers_cpp.json")
    keep = os.path.join(HERE, "SUPERSEDED_answers_cpp_symbolsonly.json")
    if not os.path.exists(keep):
        shutil.copy(p, keep)
    base = json.load(open(keep))
    assert base["complete"], "standing answers_cpp.json is not complete"
    oplist = X.W.ADMIT["cpp"]
    ids = X.accepts("cpp")

    def go():
        T = E.table("cpp")
        assert T["ops"] == oplist, "op list did not reach the table"
        return T
    T = X.with_ops("cpp", oplist, go)
    seen, summaries, files = read_rows("xw", "cpp")
    rows, n = build_rows("cpp", ids, seen, T["holders"], T["ops"])
    # ADDITIVE, and checked rather than assumed.  A row is identified by
    # (probe id, operation): the ids collide across the two menus --
    # both start at P0_0_0_0_0 -- and only the operation separates them.
    before = set(r["id"] + "|" + r["operation"] for r in base["rows"])
    new = set(r["id"] + "|" + r["operation"] for r in rows)
    assert not (before & new), \
        "word-op fold collides with %d standing rows" % len(before & new)
    assert not (set(base["operations"]) & set(oplist)), \
        "a word operation is already in cpp's standing menu"
    d = dict(base)
    d["rows"] = base["rows"] + rows
    d["operations"] = list(base["operations"]) + list(oplist)
    d["probes"] = base["probes"] + len(rows)
    d["answers"] = base["answers"] + n["answer"]
    d["raises"] = base["raises"] + n["raise_"]
    d["deaths"] = base["deaths"] + n["death"]
    d["codegen_refuse"] = base["codegen_refuse"] + n["cg"]
    d["missing"] = base["missing"] + n["miss"]
    d["lane_summaries"] = list(base["lane_summaries"]) + summaries
    d["lanes"] = base["lanes"] + len(files)
    d["complete"] = bool(base["complete"]) and n["miss"] == 0 and \
        bool(summaries)
    d["completeness"] = "COMPLETE" if d["complete"] else \
        "SHORT -- word-op fold missing %d of %d" % (n["miss"], len(rows))
    d["word_operations"] = dict(
        decision="43", operations=list(oplist),
        accepted_from="raw/vw_cpp_*.txt", executed_in="raw/xw_cpp_00.txt",
        probes=len(rows), answers=n["answer"],
        note="the standard's alternative token spellings; each must equal "
             "its symbol twin on every shared probe -- see wordop_control")
    json.dump(d, open(p, "w"))
    print("| menu | probes | answers | deaths | codegen refuse |")
    print("|---|---|---|---|---|")
    print("| cpp symbols (standing) | %d | %d | %d | %d |"
          % (base["probes"], base["answers"], base["deaths"],
             base["codegen_refuse"]))
    print("| cpp words (decision 43) | %d | %d | %d | %d |"
          % (len(rows), n["answer"], n["death"], n["cg"]))
    print("| cpp merged | %d | %d | %d | %d |"
          % (d["probes"], d["answers"], d["deaths"], d["codegen_refuse"]))
    print("gate: %s" % d["completeness"])
    return d


# ---------------------------------------------------------- 3, route C
REPAIRED = dict(ruby="rc_ruby2", php="rc_php2")


def refold_routec():
    print("\n== 3. route C re-read from the repaired runs")
    out = {}
    print("| language | probes | answers | raises | source | gate |")
    print("|---|---|---|---|---|---|")
    for lang, stem in REPAIRED.items():
        p = os.path.join(HERE, "behavior_%s_C.json" % lang)
        keep = os.path.join(
            HERE, "SUPERSEDED_behavior_%s_C_preparen.json" % lang)
        if os.path.exists(p) and not os.path.exists(keep):
            shutil.copy(p, keep)
        # l3_read.read_routec reads raw/rc_<lang>.txt by construction.
        # The repaired product is raw/rc_<lang>2.txt.  Rather than
        # swapping the two files -- the first attempt, which the mount
        # refuses -- os.path.join is patched for the length of the call,
        # so ONE reader, with its gate and its verdict-token split, is
        # used on both inputs and nothing on disk moves.
        real = os.path.join(RAW, "rc_%s.txt" % lang)
        want = os.path.join(RAW, stem + ".txt")
        oldjoin = R.os.path.join

        def join(*a):
            q = oldjoin(*a)
            return want if q == real else q
        R.os.path.join = join
        try:
            r = R.read_routec(lang)
        finally:
            R.os.path.join = oldjoin
        d = json.load(open(p))
        d["source"] = "raw/%s.txt" % stem
        d["supersedes"] = ("behavior_%s_C.json taken with the pre-repair "
                           "route-C driver, kept as %s"
                           % (lang, os.path.basename(keep)))
        d["repair"] = ("the route-C parenthesis repair, log 034 section "
                       "3.2: `__r = ((a) op (b))'.  The word-spelled "
                       "logicals bind looser than assignment in both "
                       "languages, so the unparenthesised form recorded "
                       "the LEFT OPERAND.")
        json.dump(d, open(p, "w"))
        k = r["kinds"]
        print("| %s | %d | %d | %d | %s | %s |"
              % (lang, r["probes"], k.get("ANSWER", 0), k.get("RAISE", 0),
                 stem, r["completeness"]))
        out[lang] = r
    return out


# ------------------------------------------------- the positive controls
TWIN = dict(cpp={"and": "&&", "bitand": "&", "bitor": "|",
                 "not_eq": "!=", "or": "||", "xor": "^"})


def control_cpp():
    """each c++ word must answer exactly what its symbol twin answers."""
    print("\n== control A: c++'s six word spellings against their twins")
    d = json.load(open(os.path.join(HERE, "answers_cpp.json")))
    by = {}
    for r in d["rows"]:
        cell = "%s|%s|%s|%s" % (r["lhs"]["holder"], r["lhs"]["value"],
                                r["rhs"]["holder"], r["rhs"]["value"])
        sig = (r["outcome"],
               json.dumps(r.get("result"), sort_keys=True) if
               r["outcome"] == "answer" else r.get("death", ""))
        by.setdefault(r["operation"], {})[cell] = sig
    res = {}
    print("| word | twin | shared cells | agree | disagree |")
    print("|---|---|---|---|---|")
    for w, s in sorted(TWIN["cpp"].items()):
        a, b = by.get(w, {}), by.get(s, {})
        shared = set(a) & set(b)
        agree = sum(1 for c in shared if a[c] == b[c])
        res[w] = dict(twin=s, shared=len(shared), agree=agree,
                      disagree=len(shared) - agree,
                      word_cells=len(a), twin_cells=len(b),
                      examples=[dict(cell=c, word=a[c], twin=b[c])
                                for c in sorted(shared)
                                if a[c] != b[c]][:8])
        print("| cpp.%s | cpp.%s | %d | %d | %d |"
              % (w, s, len(shared), agree, len(shared) - agree))
    ok = all(v["shared"] > 0 and v["disagree"] == 0 for v in res.values())
    print("CONTROL A %s" % ("PASSES: every c++ word answers exactly what "
                            "its symbol twin answers, on every shared cell"
                            if ok else "FAILS -- see examples in "
                            "refold_index.json"))
    return dict(passes=ok, pairs=res)


def control_ruby():
    """ruby.and must answer what ruby.&& answers, cell for cell."""
    print("\n== control B: ruby's `and' against ruby's `&&'")
    d = json.load(open(os.path.join(HERE, "behavior_ruby_C.json")))
    cells = d["cells"]
    by = {}
    for pid, v in cells.items():
        # the id ENDS with the operation and the operation may itself be
        # `|` or `||`, so split from the RIGHT on the FIRST underscore
        # that precedes a known operation.  Here only the suffix matters.
        for op in ("and", "or", "&&", "||"):
            if pid.endswith("_" + op):
                by.setdefault(op, {})[pid[:-(len(op) + 1)]] = v
                break
    res = {}
    print("| word | twin | shared | agree | differ | differ w/ address |")
    print("|---|---|---|---|---|---|")
    for w, s in (("and", "&&"), ("or", "||")):
        a, b = by.get(w, {}), by.get(s, {})
        shared = sorted(set(a) & set(b))
        diff = [c for c in shared if a[c] != b[c]]
        addr = [c for c in diff if "0x" in str(a[c]) or "0x" in str(b[c])]
        res[w] = dict(twin=s, shared=len(shared),
                      agree=len(shared) - len(diff), differ=len(diff),
                      differ_with_address=len(addr),
                      differ_without_address=len(diff) - len(addr),
                      examples=[dict(cell=c, word=a[c], twin=b[c])
                                for c in diff if c not in set(addr)][:8])
        print("| ruby.%s | ruby.%s | %d | %d | %d | %d |"
              % (w, s, len(shared), len(shared) - len(diff), len(diff),
                 len(addr)))
    ok = all(v["differ_without_address"] == 0 and v["shared"] > 0
             for v in res.values())
    print("CONTROL B %s" % (
        "PASSES: every difference between the word form and the symbol "
        "form carries a hexadecimal object address, so it is the log-034 "
        "section 4.3 recorder fault and not a disagreement"
        if ok else "FAILS -- a difference with no address in it"))
    return dict(passes=ok, pairs=res)


def main():
    idx = {}
    sw = refold_swift()
    cp = refold_cpp()
    rc = refold_routec()
    idx["swift"] = dict(probes=sw["probes"], answers=sw["answers"],
                        codegen_refuse=sw["codegen_refuse"],
                        complete=sw["complete"])
    idx["cpp"] = dict(probes=cp["probes"], answers=cp["answers"],
                      operations=len(cp["operations"]),
                      complete=cp["complete"])
    for lang, r in rc.items():
        idx[lang] = dict(probes=r["probes"], kinds=r["kinds"],
                         complete=r["complete"])
    idx["typescript_instanceof"] = dict(
        admitted_by="decision 43", accepted=0, probed=10000,
        note="EMPTY DOMAIN -- route A accepted none of the 10,000 probes, "
             "so the operation folds to no leaf.  Admitted and empty is "
             "not the same as excluded, and it is recorded here as the "
             "former.")
    idx["controls"] = dict(cpp_words=control_cpp(), ruby_and=control_ruby())
    json.dump(idx, open(os.path.join(HERE, "refold_index.json"), "w"),
              indent=1)
    print("\nwrote refold_index.json")


if __name__ == "__main__":
    main()
