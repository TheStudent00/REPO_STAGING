#!/usr/bin/env python3
"""l3_matrix.py -- the FULL VALUE MATRIX for the statically checked nine.

CORE_0_3_2 ruling 3: *every value of every holder, everywhere*.  The
acceptance runs of log_027 section 3.1 carried ONE value class per
holder and enumerated the pair space; the reason given was that a
statically checked language's verdict is a function of the holder pair
and not of the value.  That reason is an ASSUMPTION and it has never
been measured.  This file measures it: the same route-A checker, over
the same ordered holder pairs, times the FULL cross product of value
classes.

Two things follow from doing it this way rather than by executing.

  * it is the same instrument.  A verdict here is comparable, cell for
    cell, with the acceptance run's verdict, so any place where the
    value class DOES move the verdict shows up as a difference between
    two files rather than as a new kind of evidence.
  * it needs no answer.  Answers come from route C, which is a separate
    build; nothing here reads one.

Sizing, sharding and cost are printed before anything runs (ruling 4).
The lane daemon kills a script at 3600 s, so every language is SHARDED
into pieces sized from its own measured per-probe cost, and each shard
is a lane of its own.
"""

import base64
import gzip
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.join(HERE, "lanes")
os.makedirs(LANES, exist_ok=True)
sys.path.insert(0, HERE)
from l3_accept import (LANG, holders, ops, rename,          # noqa: E402
                       side_rename_types)
from l3_lanes import (DRIVER, PRELUDE, DRV_CS, KDRV_JAVA,   # noqa: E402
                      JDRV_JAVA, TDRV_JS, MODES, EXT)

# measured ms per probe, from log_027 section 3.1 (route A runs) and
# from this session's java and typescript runs.  MEASURED, not guessed.
MS = dict(typescript=0.34, dart=0.98, csharp=1.51, java=3.41, rust=6.8,
          go=17.4, swift=42.5, kotlin=52.1, cpp=60.9)
ORDER = ["typescript", "dart", "csharp", "java", "rust", "go", "swift",
         "kotlin", "cpp"]
SHARD_SECONDS = 2400.0          # 40 min, against the daemon's 3600 s kill
# /work is a 4 GB tmpfs and a tmpfs charges a whole block per file, so a
# shard's SOURCE COUNT is a cost of its own: 230,000 probe files measured
# 912 MB.  MEASURED 2026-08-18, and the reason a shard is capped by probe
# count as well as by projected time.
SHARD_PROBES = 120000


def matrix(lang):
    """every (ordered holder pair) x (ordered value-class pair) x op."""
    hs, _ = holders(lang)
    os_ = ops(lang)
    tpl = LANG[lang]
    rows = []
    for i, ha in enumerate(hs):
        va = sorted(ha["values"])
        for j, hb in enumerate(hs):
            vb = sorted(hb["values"])
            for x in range(len(va)):
                for y in range(len(vb)):
                    for k in range(len(os_)):
                        rows.append((i, j, x, y, k))
    return hs, os_, tpl, rows


def table(lang, hs, os_, tpl):
    return dict(language=lang, ops=os_, ext=EXT[lang],
                head=tpl["head"], decl=tpl["decl"], body=tpl["body"],
                tail=tpl["tail"],
                holders=[dict(form=h["form"], rep=h["rep"],
                              pre=h.get("pre", ""),
                              values=[[k, h["values"][k]]
                                      for k in sorted(h["values"])])
                         for h in hs])


ASSEMBLE = r'''
import re as _re
T = json.load(open(os.path.join(ROOT, "table.json")))
SPEC = json.load(open(os.path.join(ROOT, "shard.json")))
HS, OPS, TPL = T["holders"], T["ops"], T
LANG_ = T["language"]

def _rn(s, n):
    return _re.sub(r"\bv\b", n, s)

_DT = _re.compile(r"\b(?:record|class|interface|enum)\s+([A-Za-z_]\w*)")

def _side(decl, suffix):
    for n in sorted(set(_DT.findall(decl)), key=len, reverse=True):
        decl = _re.sub(r"\b%s\b" % _re.escape(n), n + suffix, decl)
    return decl

probes = []
for (i, j, x, y, k) in SPEC["rows"]:
    ha, hb = HS[i], HS[j]
    vca, da = ha["values"][x]
    vcb, db = hb["values"][y]
    da = _rn(da, "a"); db = _rn(db, "b")
    if LANG_ == "java":
        db = _side(db, "_b")
    pres = []
    for h, dtext in ((ha, da), (hb, db)):
        for line in (h.get("pre") or "").splitlines():
            line = line.strip()
            if not line:
                continue
            m = _re.findall(r"[A-Za-z_][A-Za-z_0-9]*", line)
            tok = m[-1] if m else ""
            if LANG_ in ("go", "rust") and tok and tok not in dtext:
                continue
            if line not in pres:
                pres.append(line)
    ident = "%d_%d_%d_%d_%d" % (i, j, x, y, k)
    src = (TPL["head"].replace("{PRE}", "\n".join(pres))
                      .replace("{ID}", ident)
           + TPL["decl"].replace("{D}", da))
    if SPEC.get("loadcheck"):
        # LOAD CHECK: the left declaration alone, no second operand and
        # no operation.  It answers the one question a value-matrix
        # split cannot answer by itself -- whether the value class moved
        # the OPERATION's verdict or simply failed to LOAD into the
        # holder (`short v = 9223372036854775807;` does not fit).  The
        # first is layer 3; the second is layer 2 leaking into it.
        src += TPL["tail"]
    else:
        src += (TPL["decl"].replace("{D}", db)
                + TPL["body"].replace("{A}", "a").replace("{B}", "b")
                             .replace("{OP}", OPS[k])
                + TPL["tail"])
    probes.append(dict(id="P" + ident, src=src))
print("probes assembled: %d (shard %d of %d)"
      % (len(probes), SPEC["shard"], SPEC["shards"]))
sys.stdout.flush()
'''


def emit(lang, shard, shards, rows, tbl, total, loadcheck=False):
    """one lane per shard."""
    name = ("ld_%s_%02d" if loadcheck else "vm_%s_%02d") % (lang, shard)
    spec = json.dumps(dict(shard=shard, shards=shards, rows=rows,
                           loadcheck=loadcheck))
    def b64(raw):
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as g:
            g.write(raw)
        b = base64.b64encode(buf.getvalue()).decode()
        return "\n".join(b[i:i+76] for i in range(0, len(b), 76))

    drv = DRIVER.replace("{LANG}", lang).replace("{EXT}", EXT[lang]) \
                .replace("{MODE}", MODES[lang])
    drv = drv.replace("{{", "{").replace("}}", "}")
    drv = drv.replace("DRV_CS", "'''" + DRV_CS + "'''") \
             .replace("KDRV_JAVA", "'''" + KDRV_JAVA + "'''") \
             .replace("JDRV_JAVA", "r'''" + JDRV_JAVA + "'''") \
             .replace("TDRV_JS", "r'''" + TDRV_JS + "'''")
    drv = drv.replace('OUT  = "/out/ac_%s.txt" % LANG',
                      'OUT  = "/out/%s.txt"' % name)
    old = ('probes = [json.loads(l) for l in open(os.path.join(ROOT, '
           '"probes.jsonl"))]\nprint("probes loaded: %d" % len(probes)); '
           'sys.stdout.flush()')
    assert old in drv, "driver probe-loading block moved"
    drv = drv.replace(old, ASSEMBLE)
    head = (PRELUDE.replace("{LANG}", lang)
                   .replace("{ROUTE}", "value matrix, route A, shard %d/%d"
                            % (shard, shards))
                   .replace("{N}", str(len(rows)))
                   .replace("{{", "{").replace("}}", "}"))
    head = head.split("base64 -d <<'B64_EOF'")[0]
    head = head.replace("ROOT=/work/ac_" + lang, "ROOT=/work/%s" % name)
    head += ("base64 -d <<'T_EOF' | gunzip > \"$ROOT/table.json\"\n%s\nT_EOF\n"
             % b64(json.dumps(tbl).encode()))
    head += ("base64 -d <<'S_EOF' | gunzip > \"$ROOT/shard.json\"\n%s\nS_EOF\n"
             % b64(spec.encode()))
    setup = ""
    if lang == "typescript":
        setup = ('if [ ! -f /persist/tv/ts5/node_modules/typescript/lib/'
                 'typescript.js ]; then\n  mkdir -p /persist/tv/ts5 && '
                 'cd /persist/tv/ts5 && npm install typescript@5 '
                 '--no-audit --no-fund >/dev/null 2>&1\nfi\n')
    # SWEEP UP.  Every lane wipes its own ROOT on entry, which is enough
    # when lanes are rare and enormous when they are twenty: /work is a
    # 4 GB tmpfs and a finished shard was still holding 1,121 MB of probe
    # sources when the next one started *(measured 2026-08-18, dart shard
    # 0)*.  A serial queue of twenty shards would hit ENOSPC part way
    # through and, on this phase's evidence, exit 0 while doing it.
    tail = ('\nrm -rf "$ROOT"\n'
            'echo "swept $ROOT; /work free: $(df -Pm /work | '
            'awk \'NR==2{print $4}\') MB"\n')
    p = os.path.join(LANES, name + ".sh")
    open(p, "w").write(head + setup + drv + tail)
    os.chmod(p, 0o755)
    return name, p


def loadcheck():
    """one probe per (holder, value class): can the holder hold it?"""
    print("| language | holders | load-check probes | projected |")
    print("|---|---|---|---|")
    plan = []
    for lang in ORDER:
        hs, _ = holders(lang)
        os_ = ops(lang)
        tpl = LANG[lang]
        rows = [(i, i, x, x, 0) for i, h in enumerate(hs)
                for x in range(len(h["values"]))]
        tbl = table(lang, hs, os_, tpl)
        name, _p = emit(lang, 0, 1, rows, tbl, len(rows), loadcheck=True)
        print("| %s | %d | %d | %.1f s |"
              % (lang, len(hs), len(rows), len(rows) * MS[lang] / 1000.0))
        plan.append(dict(language=lang, probes=len(rows), lane=name))
    json.dump(dict(plan=plan), open(os.path.join(HERE, "loadcheck_plan.json"),
                                    "w"), indent=1)


def main():
    if sys.argv[1:2] == ["--loadcheck"]:
        return loadcheck()
    which = sys.argv[1:] or ORDER
    plan = []
    print("| language | holders | ops | value-matrix probes | ms/probe "
          "(measured) | projected | shards |")
    print("|---|---|---|---|---|---|---|")
    grand = 0.0
    for lang in which:
        hs, os_, tpl, rows = matrix(lang)
        tbl = table(lang, hs, os_, tpl)
        secs = len(rows) * MS[lang] / 1000.0
        n = max(1,
                int(secs / SHARD_SECONDS) + (1 if secs % SHARD_SECONDS else 0),
                (len(rows) + SHARD_PROBES - 1) // SHARD_PROBES)
        per = (len(rows) + n - 1) // n
        grand += secs
        print("| %s | %d | %d | %d | %.2f | %.1f min | %d |"
              % (lang, len(hs), len(os_), len(rows), MS[lang], secs / 60.0, n))
        names = []
        for s in range(n):
            chunk = rows[s * per:(s + 1) * per]
            if not chunk:
                continue
            names.append(emit(lang, s, n, chunk, tbl, len(rows))[0])
        plan.append(dict(language=lang, probes=len(rows), shards=len(names),
                         lanes=names, ms_per_probe=MS[lang],
                         projected_seconds=secs))
    print("\nprojected TOTAL: %.2f hours (derived from measured per-probe "
          "costs)" % (grand / 3600.0))
    json.dump(dict(plan=plan, projected_seconds_total=grand,
                   shard_seconds=SHARD_SECONDS),
              open(os.path.join(HERE, "matrix_plan.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
