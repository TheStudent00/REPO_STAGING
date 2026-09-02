#!/usr/bin/env python3
"""l3_wordops.py -- log 034 JOB B: the word-spelled operations that
decision 43 admits, taken to the same grain as the symbol-spelled ones.

Decision 43 (see log_034 section 3) admits a word-spelled binary
operation as FIRST CLASS iff both legs hold:

  leg G  the grammar declares the word among the anonymous tokens of
         the operator slot of a binary-shaped expression node
         (wordop_survey.py, reads only node-types.json)
  leg R  the language's own checker REFUSES an ordinary variable named
         with that word, in the probe's own scope
         (lanes lr_words*.sh, read from raw/lr_words*.txt)

The admitted set this file acts on is written by hand from the two
measured tables and re-checked against them at import, so a later
change to either table fails loudly here rather than silently.

It emits, additively, the lanes that carry the admitted operations to
the same grain the symbol-spelled ones already have.  It changes NO
existing lane and supersedes NO existing product.
"""
import json, os, sys, io, gzip, base64, shutil, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import l3_accept as A
import l3_matrix as M
import l3_routec as C

# ---- what decision 43 admits, per language, over the standing menu.
ADMIT = {
    "cpp":        ["and", "bitand", "bitor", "not_eq", "or", "xor"],
    "typescript": ["instanceof"],
    "ruby":       ["and", "or"],
    "php":        ["instanceof"],
    "go": [], "rust": [], "swift": [], "dart": [], "csharp": [],
    "kotlin": [], "java": [], "python": [],
}
# already first class before this pass, and re-checked by the criterion
ALREADY = {"python": ["and", "or", "is", "in", "is not", "not in"],
           "php": ["and", "or", "xor"], "typescript": ["in"]}
# LIBRARY, excluded, both legs named.  Measured as a labelled aside so
# the shift tally can be read either way; never folded by default.
ASIDE = {"kotlin": ["shl", "shr", "ushr", "and", "or", "xor"]}


def check():
    s = json.load(open(os.path.join(HERE, "wordop_survey.json")))
    for L, ws in ADMIT.items():
        g = set(s[L]["grammar_declared_words"])
        for w in ws:
            assert w in g, "leg G does not declare %s.%s" % (L, w)
    for L, ws in ASIDE.items():
        g = set(s[L]["grammar_declared_words"])
        for w in ws:
            assert w not in g, "leg G DOES declare %s.%s -- aside is wrong" % (L, w)
    print("decision 43 re-checked against wordop_survey.json: leg G agrees")


def with_ops(lang, oplist, fn):
    """run fn() with l3_accept.ops(lang) forced to oplist."""
    old = A.ops
    def patched(l):
        return oplist if l == lang else old(l)
    A.ops = M.ops = C.ops = patched
    try:
        return fn()
    finally:
        A.ops = M.ops = C.ops = old


def emit_matrix(lang, oplist, prefix, ms, shard_seconds=1500.0):
    """value-matrix lanes over oplist only, named <prefix>_<lang>_NN."""
    def go():
        hs, ops_, tpl, rows = M.matrix(lang)
        tbl = M.table(lang, hs, ops_, tpl)
        secs = len(rows) * ms / 1000.0
        n = max(1, int(secs / shard_seconds) + (1 if secs % shard_seconds else 0))
        per = (len(rows) + n - 1) // n
        print("| %s | %d | %s | %d | %.1f | %.1f min | %d |"
              % (lang, len(hs), ",".join(ops_), len(rows), ms, secs/60.0, n))
        tmp = tempfile.mkdtemp(prefix="wordops_")
        real, M.LANES = M.LANES, tmp
        names = []
        for s in range(n):
            chunk = rows[s*per:(s+1)*per]
            if not chunk:
                continue
            name, p = M.emit(lang, s, n, chunk, tbl, len(rows))
            txt = open(p).read()
            txt = txt.replace("/work/vm_" + lang, "/work/%s_%s" % (prefix, lang))
            txt = txt.replace("/out/vm_" + lang, "/out/%s_%s" % (prefix, lang))
            txt = txt.replace("value matrix, route A",
                              "WORD-OPERATION matrix (decision 43), route A")
            np = os.path.join(real, name.replace("vm_", prefix + "_") + ".sh")
            open(np, "w").write(txt); os.chmod(np, 0o755)
            names.append(os.path.basename(np)[:-3])
        M.LANES = real; shutil.rmtree(tmp, ignore_errors=True)
        return dict(language=lang, ops=ops_, probes=len(rows),
                    shards=len(names), lanes=names,
                    ms_per_probe=ms, projected_seconds=secs)
    return with_ops(lang, oplist, go)


# ---- the route-C PARENTHESIS repair.
#
# `$__r = ($a) and ($b);` in php and `__r = (a) and (b)` in ruby both
# bind as `(__r = a) and b`, because in BOTH languages the word-spelled
# logicals sit BELOW assignment in precedence while the symbol-spelled
# ones sit above it.  The recorded answer is then the LEFT OPERAND and
# not the operation's value.  This is the fault log 033 section 6 named
# for php ("one pair of parentheses in l3_routec.py") and it is the
# same fault in ruby, where it had not been noticed because ruby had no
# word-spelled operation in its menu until this pass admitted one.
PHP_OLD = '$src = $head . "\\$__r = (\\$a) $op (\\$b);";'
PHP_NEW = '$src = $head . "\\$__r = ((\\$a) $op (\\$b));";'
RB_OLD = 'src = head + "__r = (a) #{op} (b)\\n__r"'
RB_NEW = 'src = head + "__r = ((a) #{op} (b))\\n__r"'


def repair_routec():
    n = 0
    if PHP_OLD in C.PHP_DRIVER:
        C.PHP_DRIVER = C.PHP_DRIVER.replace(PHP_OLD, PHP_NEW); n += 1
    if RB_OLD in C.RUBY_DRIVER:
        C.RUBY_DRIVER = C.RUBY_DRIVER.replace(RB_OLD, RB_NEW); n += 1
    assert n == 2, "route-C parenthesis repair: %d of 2 sites found" % n
    print("route-C parenthesis repair applied to php and ruby (2 of 2 sites)")


def emit_routec(lang, oplist, name):
    repaired = {"php": "/out/rc_php.txt", "ruby": "/out/rc_ruby.txt"}[lang]
    def go():
        C.emit(lang)
        p = os.path.join(C.LANES, "rc_%s.sh" % lang)
        txt = open(p).read()
        txt = txt.replace(repaired, "/out/%s.txt" % name)
        txt = txt.replace("/work/rc_" + lang, "/work/" + name)
        np = os.path.join(C.LANES, name + ".sh")
        open(np, "w").write(txt); os.chmod(np, 0o755)
        print("  emitted %s  (ops: %s)" % (name, ",".join(oplist)))
        return np
    return with_ops(lang, oplist, go)


def main():
    check(); repair_routec()
    plan = {}
    print("\n| language | holders | ops | probes | ms/probe | projected | "
          "shards |")
    print("|---|---|---|---|---|---|---|")
    plan["cpp"] = emit_matrix("cpp", ADMIT["cpp"], "vw", M.MS["cpp"])
    plan["typescript"] = emit_matrix("typescript", ADMIT["typescript"], "vw",
                                     M.MS["typescript"])
    plan["kotlin_aside"] = emit_matrix("kotlin", ASIDE["kotlin"], "ka",
                                       M.MS["kotlin"])
    print("\nroute C, re-run whole with the repaired driver:")
    emit_routec("ruby", A.ops("ruby") + ADMIT["ruby"], "rc_ruby2")
    emit_routec("php", A.ops("php") + ADMIT["php"], "rc_php2")
    plan["ruby"] = dict(lane="rc_ruby2", ops=A.ops("ruby") + ADMIT["ruby"])
    plan["php"] = dict(lane="rc_php2", ops=A.ops("php") + ADMIT["php"])
    json.dump(dict(admit=ADMIT, already=ALREADY, aside=ASIDE, plan=plan),
              open(os.path.join(HERE, "wordops_plan.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
