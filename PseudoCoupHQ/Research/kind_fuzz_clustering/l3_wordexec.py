#!/usr/bin/env python3
"""l3_wordexec.py -- log 035: execute the word-spelled operations that
decision 43 admitted and that route A measured a domain for.

JOB B left one thing unbuilt.  Ruby's `and`/`or` and php's `instanceof`
come free, because route C answers as it runs and `rc_ruby2`/`rc_php2`
already carry them.  C++ does not: c++ is a route-A language, so
`vw_cpp_00..02` gave its six word spellings an ACCEPT/REFUSE DOMAIN and
nothing else.  Their ANSWERS have to be executed, the same way
`ex_cpp_00` executed the symbol-spelled menu's.

Typescript's `instanceof` needs no exec lane: `vw_typescript_00`
accepted 0 of 10,000 probes, so its domain is empty and there is
nothing to run.  That is recorded in `wordexec_plan.json` rather than
passed over in silence.

The one thing that matters here, as in `l3_swiftexec.py`, is that the
accepted set and the operation list must be the WORD ones.  A probe id
`Pi_j_x_y_k` carries `k` as an index into the operation list it was
generated against, and `vw_cpp_*`'s `k` indexes
[and, bitand, bitor, not_eq, or, xor], not c++'s standing menu.
`l3_wordops.with_ops` is the same patch the matrix lanes were emitted
under, so it is reused rather than re-derived.

THE CHECK THIS RUN CARRIES.  C++'s six words are the standard's
alternative token spellings of `&&`, `&`, `|`, `!=`, `||` and `^`
(log 034 section 3.3).  Every answer here must equal its symbol twin's
answer on the same probe, bit for bit.  A single disagreement is
evidence against the machinery, not against c++.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)
import l3_exec as E
import l3_exec_lanes as L
import l3_wordops as W

PREFIX = "vw"


# ---- why this file does not just call l3_wordops.with_ops
#
# `l3_wordops.with_ops` rebinds `ops` on l3_accept, l3_matrix and
# l3_routec, which is every module the MATRIX lanes go through.  The
# EXECUTION path has a fourth: `l3_exec.py` line 51 does
# `from l3_accept import ..., ops`, which binds its own module-level
# name to the function OBJECT at import time, so rebinding
# `l3_accept.ops` afterwards does not reach it.
#
# Measured 2026-08-19, and it was measured the expensive way: the first
# `xw_cpp_00` ran with c++'s STANDING menu, so probe `P0_0_0_0_3`, whose
# `k=3` means `not_eq`, was emitted as `/` and the compiler answered
# `no match for 'operator/'`.  2,466 of 8,526 probes came back
# CODEGEN_REFUSE, and that count is the only reason the fault was seen:
# the lane exited 0 and wrote a full `__SUMMARY__`.  That product is
# quarantined as `raw/VOID_xw_cpp_00_wrongops.txt`.
def with_ops(lang, oplist, fn):
    """l3_wordops.with_ops, plus the l3_exec binding it cannot reach."""
    olde = E.ops

    def patched(l):
        return oplist if l == lang else olde(l)
    E.ops = patched
    try:
        return W.with_ops(lang, oplist, fn)
    finally:
        E.ops = olde


def accepts(lang):
    """the ACCEPT ids of the WORD-operation matrix, in id order."""
    ids, files = [], sorted(
        f for f in os.listdir(RAW)
        if f.startswith("%s_%s_" % (PREFIX, lang)) and f.endswith(".txt"))
    for fn in files:
        for line in open(os.path.join(RAW, fn)):
            if "|ACCEPT|" not in line and not line.startswith("P"):
                continue
            p = line.split("|")
            if len(p) < 2 or p[1] != "ACCEPT" or not p[0].startswith("P"):
                continue
            ids.append(tuple(int(z) for z in p[0][1:].split("_")))
    ids.sort()
    print("  %s: %d shards, %d ACCEPT probes" % (lang, len(files), len(ids)))
    return ids


def main():
    W.check()
    plan = {}
    print("\n| language | word ops | accepted | chunks | lane |")
    print("|---|---|---|---|---|")
    for lang in ("cpp", "typescript"):
        oplist = W.ADMIT[lang]
        rows = accepts(lang)
        if not rows:
            plan[lang] = dict(language=lang, ops=oplist, accepted=0,
                              lane=None,
                              note="empty domain -- route A accepted 0 "
                                   "probes, so there is nothing to execute "
                                   "and no leaf to fold")
            print("| %s | %s | 0 | - | NONE, empty domain |"
                  % (lang, ",".join(oplist)))
            continue
        nch = (len(rows) + E.CHUNK[lang] - 1) // E.CHUNK[lang]
        name = "xw_%s_00" % lang
        # emit, and CHECK that the op list reached the table the lane
        # actually carries rather than trusting that it did.  This is
        # the assertion the first run did not have.
        def go():
            seen = E.table(lang)["ops"]
            assert seen == oplist, \
                "op list did not reach l3_exec.table: %r" % (seen,)
            return L.emit(lang, 0, nch, name=name, rows=rows)
        with_ops(lang, oplist, go)
        plan[lang] = dict(language=lang, ops=oplist, accepted=len(rows),
                          chunks=nch, lane=name,
                          accepted_from="raw/%s_%s_*.txt" % (PREFIX, lang),
                          expect_codegen_refuse=0)
        print("| %s | %s | %d | %d | %s |"
              % (lang, ",".join(oplist), len(rows), nch, name))
    json.dump(plan, open(os.path.join(HERE, "wordexec_plan.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
