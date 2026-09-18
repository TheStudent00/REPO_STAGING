#!/usr/bin/env python3
"""Differential test: the 492 arch-units in java, python, ruby and javascript
against the SAME arch-units in c.

The c arch-units are the already-verified side -- `verify_arch_units.py` and
`verify_arch_units_int.py` put them against the real compiled RISC-V
behaviour -- so c is the oracle here and what this file measures is whether
the four languages added on 2026-09-16 carry the same bits.

Every arch-unit has the same shape in every language: `nparams` operand bit
patterns in, one 64-bit answer out. So one vector plan serves all of them,
and the comparison is over identical bytes:

  1. the plan is written here, in python, and dumped per unit;
  2. a C program linking the c arch-units writes the expected answers;
  3. each language reads both files and reports the first mismatch.

    python3 scripts/verify_arch_langs.py [n_random] [lang ...]
"""

import itertools
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
AU = os.path.join(BASE, "arch_units")
WORK = os.environ.get("AUV_WORK", os.path.join(
    os.environ.get("EMUL_SCRATCH", "/tmp"), "aulangs"))
LANGS = ("java", "python", "ruby", "js")
M64 = (1 << 64) - 1

# one point either side of every boundary a 64-bit register has, plus the
# 32-bit ones the `w` arch-opcodes and the psABI widening care about
EDGES = [0, 1, 2, 3, M64, M64 - 1, 1 << 63, (1 << 63) - 1, (1 << 63) + 1,
         0xffffffff, 0x80000000, 0x7fffffff, 0x100000000, 0xffffffff00000000,
         31, 32, 63, 64, 0xdeadbeefcafebabe, 0x4048f5c3, 0x3ff0000000000000]


def run(cmd, **kw):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         **kw)
    out, err = p.communicate()
    return p.returncode, out.decode(errors="replace"), err.decode(errors="replace")


class Xorshift(object):
    def __init__(self, seed):
        self.s = seed

    def __call__(self):
        s = self.s
        s ^= (s << 13) & M64
        s ^= s >> 7
        s ^= (s << 17) & M64
        self.s = s
        return s


def plan(nparams, n_rand, rng):
    if nparams == 0:
        return [[]]
    vecs = [list(c) for c in itertools.product(EDGES, repeat=nparams)] \
        if nparams <= 2 else [list(c) for c in itertools.product(EDGES[:8],
                                                                repeat=nparams)]
    vecs += [[rng() for _ in range(nparams)] for _ in range(n_rand)]
    return vecs


def units():
    """(name, entry-per-language, nparams), both layers, c as the oracle."""
    out = []
    for f, key in (("_units.json", "units"), ("_units_int.json", "units")):
        path = os.path.join(AU, f)
        if not os.path.exists(path):
            continue
        for u in json.load(open(path))[key]:
            langs = u.get("languages") or u.get("files") or {}
            if "c" not in langs:
                continue
            out.append({"name": u["name"], "n_params": u["n_params"],
                        "entries": {lg: langs[lg]["entry"]
                                    for lg in langs if lg in ("c",) + LANGS}})
    out.sort(key=lambda u: u["name"])
    return out


C_MAIN = r'''
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <inttypes.h>
@@DECLS@@

int main(int argc, char **argv) {
    if (argc != 4) return 2;
    const char *u = argv[1];
    FILE *in = fopen(argv[2], "r"), *out = fopen(argv[3], "w");
    if (!in || !out) return 3;
    char line[512];
    while (fgets(line, sizeof line, in)) {
        uint64_t a[4] = {0, 0, 0, 0};
        sscanf(line, "%" SCNx64 " %" SCNx64 " %" SCNx64 " %" SCNx64,
               &a[0], &a[1], &a[2], &a[3]);
        uint64_t r = 0;
@@ARMS@@
        else { fclose(in); fclose(out); return 4; }
        fprintf(out, "%" PRIx64 "\n", r);
    }
    fclose(in); fclose(out);
    return 0;
}
'''

JAVA_RUNNER = r'''
import java.io.*; import java.lang.reflect.*; import java.nio.file.*;
import java.util.*;
public class AuRunner {
    public static void main(String[] x) throws Exception {
        String cls = x[0], entry = x[1]; int np = Integer.parseInt(x[2]);
        Class<?>[] ps = new Class<?>[np];
        Arrays.fill(ps, long.class);
        Method m = Class.forName(cls).getMethod(entry, ps);
        BufferedReader in = new BufferedReader(new FileReader(x[3]));
        StringBuilder sb = new StringBuilder(); String line;
        while ((line = in.readLine()) != null) {
            String[] t = line.trim().isEmpty() ? new String[0]
                                               : line.trim().split("\\s+");
            Object[] a = new Object[np];
            for (int i = 0; i < np; i++) a[i] = Long.parseUnsignedLong(t[i], 16);
            sb.append(Long.toHexString((Long) m.invoke(null, a))).append('\n');
        }
        in.close(); System.out.print(sb);
    }
}
'''

PY_RUNNER = r'''
import sys
sys.path.insert(0, sys.argv[1])
fn = getattr(__import__(sys.argv[2]), sys.argv[3])
np = int(sys.argv[4])
out = []
with open(sys.argv[5]) as fh:
    for line in fh:
        t = line.split()
        out.append("%x" % (fn(*[int(v, 16) for v in t[:np]]) & ((1 << 64) - 1)))
sys.stdout.write("\n".join(out) + "\n")
'''

RB_RUNNER = r'''
$LOAD_PATH.unshift(ARGV[0])
require ARGV[1]
fn = method(ARGV[2].to_sym)
np = ARGV[3].to_i
out = []
File.foreach(ARGV[4]) do |line|
  t = line.split.map { |v| v.to_i(16) }
  out << (fn.call(*t[0, np]) & 0xffffffffffffffff).to_s(16)
end
$stdout.write(out.join("\n") + "\n")
'''

JS_RUNNER = r'''
'use strict';
const fs = require('fs'), path = require('path');
const mod = require(path.join(process.argv[2], process.argv[3] + '.js'));
const fn = mod[process.argv[4]];
const np = parseInt(process.argv[5], 10);
const M = 0xffffffffffffffffn;
const out = [];
for (const line of fs.readFileSync(process.argv[6], 'utf8').split('\n')) {
  if (np > 0 && !line.trim()) continue;
  const t = line.trim() ? line.trim().split(/\s+/).map((v) => BigInt('0x' + v)) : [];
  out.push((fn(...t.slice(0, np)) & M).toString(16));
}
process.stdout.write(out.join('\n') + '\n');
'''


def build_c(us):
    os.makedirs(WORK, exist_ok=True)
    arms = []
    for i, u in enumerate(us):
        call = "%s(%s)" % (u["entries"]["c"],
                           ", ".join("a[%d]" % k
                                     for k in range(u["n_params"])))
        arms.append('        %sif (!strcmp(u, "%s")) r = (uint64_t)(%s);'
                    % ("" if i == 0 else "else ", u["name"], call))
    decls = ["extern uint64_t %s(%s);"
             % (u["entries"]["c"],
                ", ".join(["uint64_t"] * u["n_params"]) or "void")
             for u in us]
    src = (C_MAIN.replace("@@DECLS@@", "\n".join(decls))
                 .replace("@@ARMS@@", "\n".join(arms)))
    c = os.path.join(WORK, "au_run.c")
    open(c, "w").write(src)
    exe = os.path.join(WORK, "au_run")
    # the float arch-units call the rm0 emulations, so both trees compile in
    srcs = [os.path.join(AU, "c", f)
            for f in sorted(os.listdir(os.path.join(AU, "c")))
            if f.endswith(".c")]
    srcs += [os.path.join(AU, "emul_rm0", "c", f)
             for f in sorted(os.listdir(os.path.join(AU, "emul_rm0", "c")))
             if f.endswith(".c")]
    rc, _, err = run(["clang", "-O1", "-w",
                      "-I", os.path.join(AU, "c"),
                      "-I", os.path.join(AU, "emul_rm0", "c"), c]
                     + srcs + ["-o", exe, "-lm"])
    if rc:
        raise SystemExit("c oracle build failed:\n" + err[:3000])
    return exe


def prepare(want):
    os.makedirs(WORK, exist_ok=True)
    jd = None
    if "java" in want:
        jd = os.path.join(WORK, "jc")
        os.makedirs(jd, exist_ok=True)
        open(os.path.join(WORK, "AuRunner.java"), "w").write(JAVA_RUNNER)
        srcs = [os.path.join(AU, "java", f)
                for f in sorted(os.listdir(os.path.join(AU, "java")))
                if f.endswith(".java")]
        srcs += [os.path.join(AU, "emul_rm0", "java", f)
                 for f in sorted(os.listdir(os.path.join(AU, "emul_rm0",
                                                         "java")))
                 if f.endswith(".java")]
        rc, _, err = run(["javac", "-nowarn", "-d", jd,
                          os.path.join(WORK, "AuRunner.java")] + srcs)
        if rc:
            raise SystemExit("java build failed:\n" + err[:3000])
    for name, text in (("run.py", PY_RUNNER), ("run.rb", RB_RUNNER),
                       ("run.js", JS_RUNNER)):
        open(os.path.join(WORK, name), "w").write(text)
    return jd


def run_lang(lang, jd, u, infile):
    e = u["entries"][lang]
    n = str(u["n_params"])
    if lang == "java":
        return run(["java", "-cp", jd, "AuRunner", u["name"], e, n, infile])
    if lang == "python":
        return run([sys.executable, os.path.join(WORK, "run.py"),
                    os.path.join(AU, "python"), u["name"], e, n, infile])
    if lang == "ruby":
        return run(["ruby", os.path.join(WORK, "run.rb"),
                    os.path.join(AU, "ruby"), u["name"], e, n, infile])
    return run(["node", os.path.join(WORK, "run.js"),
                os.path.join(AU, "js"), u["name"], e, n, infile])


def main():
    n_rand = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    want = [a for a in sys.argv[2:]] or list(LANGS)
    us = [u for u in units() if all(lg in u["entries"] for lg in want)]
    print("arch-units with all of %s: %d" % (",".join(want), len(us)),
          flush=True)
    exe = build_c(us)
    jd = prepare(want)
    os.makedirs(os.path.join(WORK, "vec"), exist_ok=True)
    results = {lg: {} for lg in want}
    bad_lines = []
    for k, u in enumerate(us):
        rng = Xorshift(0x9E3779B97F4A7C15)
        vecs = plan(u["n_params"], n_rand, rng)
        infile = os.path.join(WORK, "vec", u["name"] + ".in")
        expf = os.path.join(WORK, "vec", u["name"] + ".exp")
        with open(infile, "w") as fh:
            for v in vecs:
                fh.write(" ".join("%x" % x for x in v) + "\n")
        rc, _, err = run([exe, u["name"], infile, expf])
        if rc:
            raise SystemExit("c oracle failed on %s: %s" % (u["name"], err))
        exp = open(expf).read().split()
        line = "  %-32s %5d " % (u["name"], len(vecs))
        for lg in want:
            rc, out, err = run_lang(lg, jd, u, infile)
            if rc:
                results[lg][u["name"]] = {"ok": False,
                                          "error": err.strip()[:200]}
                line += " %s:ERR" % lg
                continue
            got = out.split()
            if len(got) != len(exp):
                results[lg][u["name"]] = {"ok": False,
                                          "error": "%d answers for %d vectors"
                                          % (len(got), len(exp))}
                line += " %s:LEN" % lg
                continue
            miss = [i for i, (g, e) in enumerate(zip(got, exp)) if g != e]
            if miss:
                i = miss[0]
                results[lg][u["name"]] = {
                    "ok": False, "mismatches": len(miss),
                    "first": {"inputs": ["%x" % x for x in vecs[i]],
                              "expected": exp[i], "got": got[i]}}
                line += " %s:%d" % (lg, len(miss))
            else:
                results[lg][u["name"]] = {"ok": True, "vectors": len(vecs)}
                line += " %s:ok" % lg
        if "ok" not in line.split(u["name"])[-1] or ":" in line.replace(":ok", ""):
            pass
        if any(not results[lg][u["name"]].get("ok") for lg in want):
            bad_lines.append(line)
        if k % 25 == 0 or any(not results[lg][u["name"]].get("ok")
                              for lg in want):
            print(line, flush=True)
    out = {"n_random": n_rand, "edges": len(EDGES), "oracle": "c arch-units",
           "languages": results,
           "what": "the 492 arch-units in java, python, ruby and javascript "
                   "against the same arch-units in c, over identical vectors"}
    dst = os.path.join(BASE, "measurements", "verify_arch_langs.json")
    json.dump(out, open(dst, "w"), indent=1, sort_keys=True)
    print()
    if bad_lines:
        print("units with a disagreement:")
        for b in bad_lines[:40]:
            print(b)
        print()
    for lg in want:
        ok = sum(1 for r in results[lg].values() if r.get("ok"))
        print("  %-8s %d of %d arch-units bit-identical to c" % (lg, ok,
                                                                len(us)))
    print("wrote %s" % dst)


if __name__ == "__main__":
    main()
