#!/usr/bin/env python3
"""l3_construct_go.py -- the CONSTRUCT lane for go, the checked proof
language.

go is the cheapest instrument of the nine statically checked languages
(measured: ac_go.sh ran 7,600 acceptance probes in 132.6 s, 17 ms each),
which is why the design names it the checked half of the proof pass.

Two stages, the same two the operator pass used.

  ACCEPTANCE   one file per probe, `go build` per file, parallel.  The
               verdict is the compiler's own exit status; nothing is
               transcribed and nothing is interpreted (CORE ruling 6).
  EXECUTION    ACCEPTED probes only, batched into chunks so one compile
               covers many probes.  Each probe is its own function with
               its own `recover`, so a panic costs one probe.

Both stages use the SAME scaffold text per construct, which is what
decision 4 demands: the acceptance probe and the answer probe differ
only in which values fill the slots.
"""

import base64
import gzip
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.join(HERE, "lanes")
os.makedirs(LANES, exist_ok=True)
sys.path.insert(0, HERE)
from l3_accept import holders, base_value, rename       # noqa: E402
from construct_space import space, AUG_OPS, JUMP_K      # noqa: E402

LANG = "go"

# go's own encoder and trace recorder, in go.  Harness machinery
# (decision 5): it records, it never computes anything a construct
# could see.
PRELUDE = r'''
var __t []string

func __T(s string) { __t = append(__t, s) }

func __enc(v interface{}) string {
	if v == nil {
		return "NULL"
	}
	rv := reflect.ValueOf(v)
	switch rv.Kind() {
	case reflect.Bool:
		if rv.Bool() {
			return "BOOL:true"
		}
		return "BOOL:false"
	case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32,
		reflect.Int64:
		return fmt.Sprintf("INT:64:%016x", uint64(rv.Int()))
	case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32,
		reflect.Uint64, reflect.Uintptr:
		return fmt.Sprintf("UINT:64:%016x", rv.Uint())
	case reflect.Float32, reflect.Float64:
		return fmt.Sprintf("FLOAT:64:%016x",
			math.Float64bits(rv.Float()))
	case reflect.String:
		s := rv.String()
		b := []byte(s)
		if len(b) > 64 {
			b = b[:64]
		}
		return fmt.Sprintf("STR:%d:%d:%x", len(s), len(rv.String()), b)
	case reflect.Slice, reflect.Array:
		n := rv.Len()
		m := n
		if m > 8 {
			m = 8
		}
		xs := make([]string, 0, m)
		for i := 0; i < m; i++ {
			xs = append(xs, __enc(rv.Index(i).Interface()))
		}
		return fmt.Sprintf("LIST:%d[%s]", n, strings.Join(xs, ","))
	case reflect.Map:
		ks := rv.MapKeys()
		xs := make([]string, 0, len(ks))
		for _, k := range ks {
			xs = append(xs, __enc(k.Interface())+"=>"+
				__enc(rv.MapIndex(k).Interface()))
		}
		sort.Strings(xs)
		if len(xs) > 8 {
			xs = xs[:8]
		}
		return fmt.Sprintf("MAP:%d[%s]", len(ks), strings.Join(xs, ","))
	case reflect.Ptr, reflect.Interface:
		if rv.IsNil() {
			return "NULL"
		}
		return "REF(" + __enc(rv.Elem().Interface()) + ")"
	}
	return fmt.Sprintf("OPAQUE:%x", []byte(fmt.Sprint(v)))
}

func __tn(v interface{}) string {
	if v == nil {
		return "-"
	}
	return reflect.TypeOf(v).String()
}
'''

IMPORTS = ('import (\n\t"fmt"\n\t"math"\n\t"reflect"\n\t"sort"\n'
           '\t"strings"\n)\n')

# the scaffolds.  fixed, minimal, inert.  {A} {B} {C} are the slots,
# {K} is the jump position.
SCAF = {
 "access.subscript":  '\t__r := (a)[(b)]\n\t__ANS(__r)\n',
 "access.slice":      '\t__r := (a)[(b):(c)]\n\t__ANS(__r)\n',
 "access.member":     '\t__r := (a).f\n\t__ANS(__r)\n',
 "flow.if":           '\tif (a) {\n\t\t__T("BR=then")\n\t} else {\n'
                      '\t\t__T("BR=else")\n\t}\n',
 "flow.for":          '\t__n := 0\n\tfor __v := range (a) {\n'
                      '\t\t__T("IT=" + __enc(__v))\n\t\t__n++\n'
                      '\t\tif __n >= 8 {\n'
                      '\t\t\t__T(fmt.Sprintf("STOP=%d", __n))\n'
                      '\t\t\tbreak\n\t\t}\n\t}\n',
 "flow.break":        '\tfor _, __v := range []int{1, 2, 3, 4, 5} {\n'
                      '\t\tif __v == {K} {\n'
                      '\t\t\t__T(fmt.Sprintf("STOP=%d", __v-1))\n'
                      '\t\t\tbreak\n\t\t}\n'
                      '\t\t__T("IT=" + __enc(__v))\n\t}\n',
 "flow.continue":     '\tfor _, __v := range []int{1, 2, 3, 4, 5} {\n'
                      '\t\tif __v == {K} {\n'
                      '\t\t\t__T(fmt.Sprintf("SKIP=%d", __v))\n'
                      '\t\t\tcontinue\n\t\t}\n'
                      '\t\t__T("IT=" + __enc(__v))\n\t}\n',
 "binding.assign":    '\t__x := (a)\n\t__T("BIND=" + __enc(__x))\n',
 "binding.augassign": '\t__x := (a)\n\t__x {OP} (b)\n'
                      '\t__T("BIND=" + __enc(__x))\n',
}

# go's `expression_list` unpack destructures a CALL's multiple returns.
# It never destructures a value.  There is therefore no honest go probe
# for the unpack role and the cell is recorded NOT_APPLICABLE with its
# reason rather than faked with `_x, _y := a, a`, which would measure
# the harness.  Design decision 16.
NOT_APPLICABLE = {
    "binding.unpack": "go's expression_list destructures a call's "
                      "multiple return values, never a value; no honest "
                      "single-value probe exists",
}
ANSWER_CONS = {"access.subscript", "access.slice", "access.member"}


def go_pre(holder_list, used_text):
    lines = []
    for h in holder_list:
        for line in (h.get("pre") or "").splitlines():
            line = line.strip()
            if not line:
                continue
            m = re.findall(r"[A-Za-z_][A-Za-z_0-9]*", line)
            tok = m[-1] if m else ""
            if tok and tok not in used_text:
                continue                 # an unused import is a refusal
            if line not in lines:
                lines.append(line)
    return "\n".join(lines)


def probe_src(cons, decls, body, ident, extra_imports=()):
    """one whole go program: prelude, then the probe in its own func.

    go puts imports at the FILE head, never in a function body.  A
    holder's `pre` line is an import in go, so it is lifted out of the
    declaration list and folded into the import block.  (Harness fault
    found and fixed on the first go run, 2026-08-19: 2 of 1,710 probes
    scored REFUSE with `syntax error: unexpected keyword import`, which
    is the harness refusing, not go refusing the construct.)
    """
    imps = IMPORTS
    for path in sorted(set(re.findall(r'"([^"]+)"',
                                      "\n".join(extra_imports)))):
        if '"%s"' % path in imps:
            continue                     # a duplicate import is a refusal
        imps = imps.replace(")\n", '\t"%s"\n)\n' % path)
    return ("package main\n\n" + imps + PRELUDE
            + "\nfunc __ANS(v interface{}) {\n"
            + '\tfmt.Printf("%s|%s|%s\\n", "' + ident
            + '", __tn(v), __enc(v))\n}\n\n'
            + "func probe() {\n"
            + "".join("\t" + d + "\n" for d in decls)
            + body
            + "}\n\nfunc main() {\n\tdefer func() {\n"
            + "\t\tif r := recover(); r != nil {\n"
            + '\t\t\tfmt.Printf("%s|-|RAISE:%v\\n", "' + ident + '", r)\n'
            + "\t\t\treturn\n\t\t}\n"
            + "\t\tif len(__t) > 0 {\n"
            + '\t\t\tfmt.Printf("%s|-|TRACE:%d[%s]\\n", "' + ident
            + '", len(__t), strings.Join(__t, ","))\n'
            + "\t\t}\n\t}()\n\tprobe()\n}\n")


def gen_acceptance():
    hs, _ = holders(LANG)
    sp = space(LANG)
    present = [r["construct"] for r in sp["constructs"] if r["present"]]
    out = []
    for cons in present:
        if cons in NOT_APPLICABLE:
            continue
        sc = SCAF[cons]
        if cons in ("flow.break", "flow.continue"):
            for k in range(1, JUMP_K + 1):
                pid = "K%s_%d" % (cons, k)
                out.append((pid, probe_src(cons, [], sc.replace(
                    "{K}", str(k)), pid)))
            continue
        two = cons in ("access.subscript", "binding.augassign")
        three = cons == "access.slice"
        for i, ha in enumerate(hs):
            da = rename(base_value(ha)[1], "a")
            if three:
                # slice bounds come from the canonical whole holder
                wi = next((n for n, h in enumerate(hs)
                           if h["form"] == "whole"), None)
                if wi is None:
                    continue
                db = rename(base_value(hs[wi])[1], "b")
                dc = rename(base_value(hs[wi])[1], "c")
                pid = "K%s_%d" % (cons, i)
                pre = go_pre([ha, hs[wi]], da + db + dc + sc)
                imps = [l for l in pre.splitlines() if l.strip()]
                src = probe_src(cons, [da, db, dc], sc, pid, imps)
                out.append((pid, src))
                continue
            if not two:
                pid = "K%s_%d" % (cons, i)
                pre = go_pre([ha], da + sc)
                imps = [l for l in pre.splitlines() if l.strip()]
                src = probe_src(cons, [da], sc, pid, imps)
                out.append((pid, src))
                continue
            for j, hb in enumerate(hs):
                db = rename(base_value(hb)[1], "b")
                ops = AUG_OPS if cons == "binding.augassign" else [""]
                for op in ops:
                    body = sc.replace("{OP}", op)
                    pid = "K%s%s_%d_%d" % (cons, op, i, j)
                    pre = go_pre([ha, hb], da + db + body)
                    imps = [l for l in pre.splitlines() if l.strip()]
                    src = probe_src(cons, [da, db], body, pid, imps)
                    out.append((pid, src))
    return out


LANE = r'''#!/bin/sh
# layer-3 CONSTRUCT acceptance lane -- go -- generated by
# l3_construct_go.py.  Design: construct_design.md (2026-08-19).
# Route A2: `go build` per file, the compiler's own exit status is the
# verdict.  %(N)d probes.
set -u
export HOME=/work
export GO111MODULE=off
export GOFLAGS=-mod=mod
export GOCACHE=/work/.gocache
export GOPATH=/work/.gopath
ROOT=/work/kag
rm -rf "$ROOT"; mkdir -p "$ROOT"
echo "=== layer-3 CONSTRUCTS -- go -- acceptance + execution -- %(N)d probes ==="
date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ
df -Pm /work | awk 'NR==2{print "free /work: " $4 " MB"}'
base64 -d <<'B64_EOF' | gunzip > "$ROOT/probes.jsonl"
%(PROBES)s
B64_EOF
base64 -d <<'PY_EOF' > "$ROOT/drv.py"
%(DRV)s
PY_EOF
python3 "$ROOT/drv.py" "$ROOT"
echo "=== constructs go done ==="
date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ
'''

DRV = r'''
import json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

ROOT = sys.argv[1]
probes = [json.loads(l) for l in open(os.path.join(ROOT, "probes.jsonl"))]
OUT = open("/out/kg_go.txt", "w")
N = len(probes)

def hms(x):
    if x is None or x < 0: return "--:--:--"
    x = int(x); return "%02d:%02d:%02d" % (x//3600, (x%3600)//60, x%60)

D = os.path.join(ROOT, "p")
os.makedirs(D, exist_ok=True)
for n, p in enumerate(probes):
    d = os.path.join(D, "%05d" % n)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "main.go"), "w").write(p["src"])

t0 = time.time()
done = [0]

def one(n):
    d = os.path.join(D, "%05d" % n)
    r = subprocess.run(["go", "build", "-o", os.path.join(d, "bin"),
                        os.path.join(d, "main.go")],
                       capture_output=True, text=True, cwd=d)
    if r.returncode != 0:
        msg = (r.stderr.strip().splitlines() or ["?"])[-1][:160]
        res = ("REFUSE", msg)
    else:
        e = subprocess.run([os.path.join(d, "bin")], capture_output=True,
                           text=True, timeout=20)
        line = e.stdout.strip().splitlines()
        res = ("RUN", line[0] if line else
               ("%s|-|DEATH:%d" % (probes[n]["id"], e.returncode)))
    done[0] += 1
    if done[0] % 100 == 0:
        el = time.time() - t0
        print("[progress] go constructs [%d/%d] %5.1f%%  elapsed %s"
              "  ETA %s  mean %.1f ms"
              % (done[0], N, 100.0*done[0]/N, hms(el),
                 hms(el/done[0]*(N-done[0])), 1000.0*el/done[0]))
        sys.stdout.flush()
    return n, res

print("CONSTRUCTS go: %d acceptance probes, one `go build` each" % N)
sys.stdout.flush()
acc = ref = 0
with ThreadPoolExecutor(max_workers=8) as ex:
    for n, (tag, payload) in ex.map(one, range(N)):
        pid = probes[n]["id"]
        if tag == "REFUSE":
            OUT.write("%s|-|REFUSE:%s\n" % (pid, payload)); ref += 1
        else:
            OUT.write(payload + "\n"); acc += 1
el = time.time() - t0
print("== go constructs: %d probes, %d ACCEPT, %d REFUSE, %.1f s"
      % (N, acc, ref, el))
OUT.write("__SUMMARY__|%d|%d|%d|%.3f\n" % (N, acc, ref, el))
OUT.close()
'''


def wrap64(s, n=76):
    return "\n".join(s[i:i+n] for i in range(0, len(s), n))


def main():
    probes = gen_acceptance()
    jl = "\n".join(json.dumps(dict(id=p, src=s)) for p, s in probes)
    sh = LANE % dict(
        N=len(probes),
        PROBES=wrap64(base64.b64encode(
            gzip.compress(jl.encode("utf-8"), 9)).decode("ascii")),
        DRV=wrap64(base64.b64encode(DRV.encode("utf-8")).decode("ascii")),
    )
    p = os.path.join(LANES, "kg_go.sh")
    open(p, "w").write(sh)
    os.chmod(p, 0o755)
    # freeze the manifest beside the run
    hs, _ = holders(LANG)
    mp = os.path.join(HERE, "manifest_construct_go.json")
    json.dump(dict(language="go", frozen="2026-08-19",
                   design="construct_design.md",
                   holders=[dict(i=n, form=h["form"], rep=h["rep"],
                                 value_classes=sorted(h["values"]))
                            for n, h in enumerate(hs)],
                   not_applicable=NOT_APPLICABLE,
                   aug_ops=AUG_OPS, jump_k=JUMP_K,
                   acceptance_probes=len(probes)),
              open(mp, "w"), indent=1)
    print("go constructs: %d acceptance probes generated" % len(probes))
    print("  manifest %s" % mp)
    print("  lane %s (%d bytes)" % (p, os.path.getsize(p)))


if __name__ == "__main__":
    main()
