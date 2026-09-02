#!/usr/bin/env python3
"""l3_interval_c.py -- BREAK THE DIAGONAL.  Emit the two extra interval
lanes the owner ruled on 2026-08-21 (ruling C), for the two pilot languages
(rust, static; ruby, open dispatch / route C).

The log-049 sweep paired sample k with sample k, so every probe on a
same-ladder row was `v OP v` -- the DIAGONAL.  That is why `rust.-` and
`ruby.<=>` were indistinguishable (both answer 0 on the whole ladder)
and why `rust.+ ~ rust.-` read 1/32.  the owner's ruling C adds two more
pairings, as ADDITIONAL rows with distinct interval_id spellings.  The
diagonal rows are NOT overwritten and `matrices_interval/` is not
touched; the new rows land in `matrices_interval_c/` under the SAME ten
columns and the SAME canon rules.

  C1  SHIFTED   `x_k OP x_{(k+1) mod 32}`.  32 more probes per row and
                no new values -- the ladder already carries every point,
                only the pairing changes.  interval_id `IV32:<a>|<b>:shift`.

  C2  COMPOSITION (one level)  `op(op(x_k, x_k'), op(x_k, x_k'))` --
                each operator's own outputs fed back through itself.
                The composed operands are OUTPUT values, which mostly
                do not land on ladder points, so this is a real probe
                run AT the composed points.  interval_id
                `IV32:<a>|<b>:comp1`.

                Where an operand of the composition DECLINES the
                composed probe is NOT RUN and the position is excluded
                (ruling B).  ruby detects this itself and reports the
                operand's own outcome under the kind `RAISEOP`; rust
                gets the same effect for free, because a panic while
                computing the operand unwinds the whole probe function
                and is caught as `RAISE:panic`.

TYPE VALIDITY OF THE COMPOSITION (rust only).  `op(y, y)` has to
typecheck.  y's type is read out of the diagonal lane output
(`raw/iv_rust_00.txt`, whose answered lines carry
`std::any::type_name`), and the composition is emitted only when
`(op, ty, ty)` is an ACCEPT cell in `acceptance_rust_A2.json`.  No
cast-and-catch, no speculative compile: 110 of the 116 accepted numeric
cells compose, and the 6 that do not are the `..` cells, whose output is
a `Range` and not a holder in the table at all.  ruby is route C and
has no such question -- everything is eval'd.

BUILD-FAILURE BISECTION (rust).  The log-049 driver marked every probe
in a failed chunk BUILDFAIL.  With a composed expression in the chunk
that is too blunt, so this driver bisects a failing chunk down to the
individual probe.  Compile invocations are counted and reported, since
the owner explicitly wants to know how many files get compiled and why a run
takes the time it does.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.
"""

import base64
import collections
import gzip
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

LANES = os.path.join(HERE, "lanes")
DROP = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                    "SandboxDesign", "agent", "drop"))
RAW = os.path.join(HERE, "raw")

from l3_accept import holders, ops                          # noqa: E402
from l3_exec import RT_RUST                                 # noqa: E402
import l3_interval_values as IV                             # noqa: E402
import l3_interval_gen as G                                 # noqa: E402

N = IV.N_SAMPLES
CHUNK = 1500                     # probes per compiled file, as the pilot

# the shifted pairing: rhs sample index for lhs sample index s
SHIFT = 1


def shift_index(s):
    return (s + SHIFT) % N


def b64gz(text):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as g:
        g.write(text.encode("utf-8"))
    return base64.b64encode(buf.getvalue()).decode("ascii")


def wrap(s, width=76):
    return "\n".join(s[i:i + width] for i in range(0, len(s), width))


# ------------------------------------------------------------------
# rust: the output type of every accepted numeric cell, read from the
# diagonal lane output -- no new measurement, no guess
# ------------------------------------------------------------------

RUST_TYPE_HOLDER = {"bool": "bool", "i32": "i32", "i64": "i64",
                    "u64": "u64", "i128": "i128", "f64": "f64",
                    "f32": "f32"}


def rust_output_types():
    """(op index, lhs index, rhs index) -> rust type_name of the answer."""
    p = None
    for d in (os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                           "SandboxDesign", "agent", "out")),
              RAW):
        q = os.path.join(d, "iv_rust_00.txt")
        if os.path.exists(q):
            p = q
            break
    if p is None:
        raise SystemExit("diagonal rust lane output not found")
    ty = {}
    for line in open(p):
        line = line.rstrip("\n")
        if line.startswith("__SUMMARY__") or not line:
            continue
        pid, _, rest = line.partition("|")
        tn = rest.partition("|")[0]
        if tn == "-":
            continue
        k, i, j, _s = pid[1:].split("_")
        ty[(int(k), int(i), int(j))] = tn
    return ty


def rust_plan():
    """(shift cells, comp cells, why-skipped counter)."""
    op_list = ops("rust")
    cells = G.rust_cells()
    acc = json.load(open(os.path.join(HERE, "acceptance_rust_A2.json")))
    verdict = {}
    for cell in acc["cells"].values():
        verdict[(cell["operation"], cell["lhs"]["holder"],
                 cell["rhs"]["holder"])] = cell["verdict"]
    ty = rust_output_types()
    shift = [(op, i, j) for (op, i, j) in cells]
    comp, skipped = [], collections.Counter()
    for (op, i, j) in cells:
        k = op_list.index(op)
        tn = ty.get((k, i, j))
        if tn is None:
            skipped["no answered sample on the diagonal"] += 1
            continue
        h = RUST_TYPE_HOLDER.get(tn)
        if h is None:
            skipped["output type is not a holder in the table (%s)"
                    % tn.split("<")[0]] += 1
            continue
        if verdict.get((op, h, h)) != "ACCEPT":
            skipped["`%s %s %s` is not an ACCEPT cell" % (h, op, h)] += 1
            continue
        comp.append((op, i, j))
    return shift, comp, skipped


# ------------------------------------------------------------------
# rust lane
# ------------------------------------------------------------------

RUST_SH = r'''#!/bin/sh
# layer-3 INTERVAL lane -- rust -- ruling C (shifted + composed) --
# generated by Research/kind_fuzz_clustering/l3_interval_c.py .
# Do not hand-edit.  Static path: the ACCEPTED numeric holder pairs
# only; acceptance is NOT re-run (every ladder sample is inside its own
# holder's range, and every composed operand is a value the holder
# already produced).
set -u
export HOME=/work
ROOT=/work/iv_rust_c0
rm -rf "$ROOT"; mkdir -p "$ROOT"
echo "=== layer-3 INTERVAL ruling C -- rust -- __NP__ probes ==="
date -u +%Y-%m-%dT%H:%M:%SZ
df -Pm /work | awk 'NR==2{print "free /work: " $4 " MB"}'
base64 -d <<'T_EOF' | gunzip > "$ROOT/table.json"
__TABLE__
T_EOF
base64 -d <<'X_EOF' | gunzip > "$ROOT/rt.txt"
__RT__
X_EOF
python3 - "$ROOT" <<'PY_EOF'
__DRIVER__
PY_EOF
rm -rf "$ROOT"
echo "swept $ROOT; /work free: $(df -Pm /work | awk 'NR==2{print $4}') MB"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== interval ruling-C lane rust done ==="
'''

RUST_DRIVER = r'''
import json, os, shutil, subprocess, sys, time

ROOT = sys.argv[1]
OUT = "/out/iv_rust_c0.txt"

T = json.load(open(os.path.join(ROOT, "table.json")))
RTX = open(os.path.join(ROOT, "rt.txt")).read()
HOLD = {h["i"]: h for h in T["holders"]}
OPS = T["ops"]
NS = T["n_samples"]
SHIFT = T["shift"]
CH = T["chunk"]

ALLOW = ("#![allow(unused, non_snake_case, non_camel_case_types, "
         "unused_parens, unused_mut, unused_variables, dead_code, "
         "unconditional_panic, arithmetic_overflow)]\n")

# ---- probe list.  A probe is (id, fn name, body lines, op).
probes = []
for (op, i, j) in T["shift_cells"]:
    k = OPS.index(op)
    for s in range(NS):
        t = (s + SHIFT) % NS
        pid = "S%d_%d_%d_%d" % (k, i, j, s)
        probes.append((pid, "s_%d_%d_%d_%d" % (k, i, j, s),
                       [HOLD[i]["a"][s], HOLD[j]["b"][t],
                        "let _r = (a) %s (b);" % op]))
for (op, i, j) in T["comp_cells"]:
    k = OPS.index(op)
    for s in range(NS):
        pid = "C%d_%d_%d_%d" % (k, i, j, s)
        # the composed operands are the operator's OWN outputs at this
        # ladder point; binding y and reusing it is exactly
        # op(op(x,x'), op(x,x')) and needs no literal round-trip
        probes.append((pid, "c_%d_%d_%d_%d" % (k, i, j, s),
                       [HOLD[i]["a"][s], HOLD[j]["b"][s],
                        "let y = (a) %s (b);" % op,
                        "let _r = (y) %s (y);" % op]))

print("interval ruling C rust: %d shifted cells + %d composed cells, "
      "%d samples each = %d probes"
      % (len(T["shift_cells"]), len(T["comp_cells"]), NS, len(probes)))
sys.stdout.flush()

COMPILES = {"n": 0, "s": 0.0}


def build_src(ps):
    src = ALLOW + RTX + "\n"
    for p in ps:
        src += "// __PROBE__ %s\nfn %s() {\n" % (p[0], p[1])
        for ln in p[2]:
            src += "    %s\n" % ln
        src += '    _emit("%s", &_r);\n}\n' % p[0]
    src += "// __PROBE__ -\n"
    src += "\nfn main() {\n    std::panic::set_hook(Box::new(|_| {}));\n"
    src += "    let ps: Vec<(&str, fn())> = vec![\n"
    for p in ps:
        src += '        ("%s", %s),\n' % (p[0], p[1])
    src += "    ];\n"
    src += "    let av: Vec<String> = std::env::args().collect();\n"
    src += ("    let s: usize = if av.len() > 1 "
            "{ av[1].parse().unwrap_or(0) } else { 0 };\n")
    src += "    for i in s..ps.len() {\n        let (id, f) = ps[i];\n"
    src += ("        if std::panic::catch_unwind(f).is_err() "
            '{ println!("{}|-|RAISE:panic", id); }\n    }\n')
    src += '    println!("__END__");\n}\n'
    return src


def compile_chunk(d, ps):
    """returns (ok, seconds, stderr)."""
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    open(os.path.join(d, "chunk.rs"), "w").write(build_src(ps))
    t = time.time()
    r = subprocess.run(["rustc", "-C", "debug-assertions=on",
                        "-C", "opt-level=0", "-o", d + "/bin",
                        d + "/chunk.rs"],
                       capture_output=True, text=True, cwd=d, timeout=1800)
    el = time.time() - t
    COMPILES["n"] += 1
    COMPILES["s"] += el
    return (r.returncode == 0), el, ((r.stderr or "") + (r.stdout or ""))


def run_binary(d, ps, out):
    """run the compiled chunk, restarting past any probe that stops the
    process; returns (answers, raises, aborts, restarts, seconds)."""
    ids = [p[0] for p in ps]
    pos = dict((p, k) for k, p in enumerate(ids))
    got = {}
    start = 0
    restarts = 0
    t = time.time()
    while start < len(ids) and restarts < 500:
        pr = subprocess.Popen([d + "/bin", str(start)],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True,
                              cwd=d, bufsize=1)
        last = start - 1
        ended = False
        for line in pr.stdout:
            line = line.rstrip("\n")
            if line == "__END__":
                ended = True
                continue
            if "|" not in line:
                continue
            pid = line.split("|", 1)[0]
            k = pos.get(pid)
            if k is None:
                continue
            got[pid] = line
            if k > last:
                last = k
        pr.wait()
        if ended or last >= len(ids) - 1:
            break
        nxt = last + 1
        got[ids[nxt]] = "%s|-|ABORT:rc%s" % (ids[nxt], pr.returncode)
        start = nxt + 1
        restarts += 1
    el = time.time() - t
    a = r_ = ab = 0
    for pid in ids:
        line = got.get(pid, "%s|-|MISSING" % pid)
        out.write(line + "\n")
        if "|-|RAISE:" in line:
            r_ += 1
        elif "|-|ABORT:" in line:
            ab += 1
        elif "|-|MISSING" in line:
            pass
        else:
            a += 1
    out.flush()
    return a, r_, ab, restarts, el


def handle(d, ps, out, depth=0):
    """compile ps; on failure BISECT rather than condemning 1500 probes
    to BUILDFAIL.  Returns (answers, raises, aborts, buildfail,
    restarts, build_s, run_s)."""
    ok, tb, err = compile_chunk(d, ps)
    if ok:
        a, r_, ab, rs, tr = run_binary(d, ps, out)
        shutil.rmtree(d, ignore_errors=True)
        return a, r_, ab, 0, rs, tb, tr
    if len(ps) == 1:
        out.write("%s|-|BUILDFAIL\n" % ps[0][0])
        out.flush()
        open("/out/iv_rust_c0.compilefail.%s.txt" % ps[0][0], "w").write(
            err[:100000])
        shutil.rmtree(d, ignore_errors=True)
        print("   !! BUILDFAIL on a single probe: %s" % ps[0][0])
        sys.stdout.flush()
        return 0, 0, 0, 1, 0, tb, 0.0
    print("   !! chunk of %d failed to build; bisecting (depth %d)"
          % (len(ps), depth))
    sys.stdout.flush()
    shutil.rmtree(d, ignore_errors=True)
    h = len(ps) // 2
    acc = [0, 0, 0, 0, 0, tb, 0.0]
    for half, sub in enumerate((ps[:h], ps[h:])):
        got = handle(d + "_%d%d" % (depth, half), sub, out, depth + 1)
        for x in range(7):
            acc[x] += got[x]
    return tuple(acc)


chunks = [probes[x:x + CH] for x in range(0, len(probes), CH)]
print("chunking: %d probes -> %d chunk files, at most %d probes per file"
      % (len(probes), len(chunks), CH))
sys.stdout.flush()

out = open(OUT, "w")
t0 = time.time()
answers = raises = aborts = buildfail = restarts = 0
build_s = run_s = 0.0
for ci, ps in enumerate(chunks):
    d = os.path.join(ROOT, "c%03d" % ci)
    a, r_, ab, bf, rs, tb, tr = handle(d, ps, out)
    answers += a; raises += r_; aborts += ab
    buildfail += bf; restarts += rs
    build_s += tb; run_s += tr
    print("[progress] rust chunk %d/%d  %d probes  build %.2fs  run %.2fs"
          "  elapsed %.1fs  restarts %d"
          % (ci + 1, len(chunks), len(ps), tb, tr, time.time() - t0, rs))
    sys.stdout.flush()

el = time.time() - t0
out.write("__SUMMARY__|rust|%d|%d|%d|%d|%d|%.3f\n"
          % (len(probes), answers, raises, aborts, buildfail, el))
out.write("__TIMING__|rust|chunk_files=%d|probes=%d|chunk_cap=%d|"
          "compile_invocations=%d|compile_s=%.3f|execute_s=%.3f|"
          "other_s=%.3f|total_s=%.3f|restarts=%d\n"
          % (len(chunks), len(probes), CH, COMPILES["n"], COMPILES["s"],
             run_s, el - COMPILES["s"] - run_s, el, restarts))
out.close()
print("== interval ruling C rust: %d probes, %d answers, %d raises, "
      "%d aborts, %d buildfail, %.2f s"
      % (len(probes), answers, raises, aborts, buildfail, el))
print("== TIMING rust: %d chunk FILES compiled (cap %d probes per file), "
      "%d compile invocations totalling %.2f s; execution %.2f s; "
      "driver overhead %.2f s; wall %.2f s"
      % (len(chunks), CH, COMPILES["n"], COMPILES["s"], run_s,
         el - COMPILES["s"] - run_s, el))
'''


def emit_rust(smoke=False):
    tab = G.numeric_table("rust")
    shift, comp, skipped = rust_plan()
    if smoke:
        shift, comp = shift[:3], comp[:3]
    payload = dict(language="rust", ops=ops("rust"), n_samples=N,
                   holders=tab, shift_cells=shift, comp_cells=comp,
                   shift=SHIFT, chunk=CHUNK)
    nprobe = (len(shift) + len(comp)) * N
    sh = (RUST_SH
          .replace("__TABLE__", wrap(b64gz(json.dumps(payload))))
          .replace("__RT__", wrap(b64gz(RT_RUST)))
          .replace("__DRIVER__", RUST_DRIVER)
          .replace("__NP__", str(nprobe)))
    name = "iv_rust_c_smoke.sh" if smoke else "iv_rust_c0.sh"
    if smoke:
        sh = sh.replace("iv_rust_c0", "iv_rust_c_smoke")
    return name, sh, len(shift), len(comp), skipped, nprobe


# ------------------------------------------------------------------
# ruby lane -- ONE process, both variants, as the pilot ran one process
# ------------------------------------------------------------------

RUBY_SH = """#!/bin/sh
# layer-3 INTERVAL lane -- ruby -- ruling C (shifted + composed) --
# generated by Research/kind_fuzz_clustering/l3_interval_c.py .
# Do not hand-edit.
set -u
export HOME=/work
ROOT=/work/iv_ruby_c0
rm -rf "$ROOT"; mkdir -p "$ROOT"
echo "=== layer-3 INTERVAL ruling C -- ruby -- __NP__ probes ==="
date -u +%Y-%m-%dT%H:%M:%SZ
base64 -d <<'T_EOF' | gunzip > "$ROOT/table.json"
__TABLE__
T_EOF
base64 -d <<'DRV_EOF' > "$ROOT/drv.rb"
__DRIVER__
DRV_EOF
python3 - "$ROOT" <<'PY_EOF'
__RUNNER__
PY_EOF
rm -rf "$ROOT"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== interval ruling-C lane ruby done ==="
"""

RUBY_DRIVER = r"""ROOT = ARGV[0]
START = (ARGV[1] || "0").to_i
require 'json'
require 'bigdecimal'
$VERBOSE = nil            # ruby's "in a**b, b may be too big" warning
begin
  Process.setrlimit(Process::RLIMIT_AS, 2 * 1024 * 1024 * 1024)
rescue StandardError
end
T = JSON.parse(File.read(File.join(ROOT, "table.json")))
HS = T["holders"]; OPS = T["ops"]; NS = T["n_samples"]; SHIFT = T["shift"]

BIGBITS = 4096
TOPBITS = 512

def _top(a)
  bl = a.bit_length
  [bl, (bl > TOPBITS ? (a >> (bl - TOPBITS)) : a).to_s(16)]
end

def ser(r)
  case r
  when Integer
    a = r.abs
    if a.bit_length > BIGBITS
      bl, hx = _top(a)
      "BIGNUM:#{r < 0 ? -1 : 1}:#{bl}:#{hx}"
    else
      "Integer:#{r}"
    end
  when Rational
    n = r.numerator; d = r.denominator
    if n.abs.bit_length > BIGBITS || d.bit_length > BIGBITS
      nb, nh = _top(n.abs); db, dh = _top(d)
      "BIGRAT:#{n < 0 ? -1 : 1}:#{nb}:#{nh}:#{db}:#{dh}"
    else
      "Rational:#{n}/#{d}"
    end
  when Float
    "Float:#{r.inspect}"
  when BigDecimal
    s = r.to_s
    s.length > 4000 ? "BIGDEC:#{r.sign}:#{r.exponent}:#{s[0, 200]}" : "BigDecimal:#{s}"
  when String
    "String:#{r.length > 2000 ? r[0, 2000] : r}"
  else
    "#{r.class}:#{r.inspect[0, 400]}"
  end
end

# eval in a fresh binding each time so `a`, `b` never leak between probes
def pair(da, db, op)
  eval(da + "\n" + db + "\n((a) #{op} (b))", TOPLEVEL_BINDING.dup)
end

def compose(y, op)
  b = TOPLEVEL_BINDING.dup
  b.local_variable_set(:__y, y)
  eval("((__y) #{op} (__y))", b)
end

PROBES = []
HS.each do |ha|
  HS.each do |hb|
    OPS.each_with_index do |op, k|
      NS.times do |s|
        # C1 shifted: x_s OP x_{(s+SHIFT) mod NS}
        PROBES << ["S#{k}_#{ha['i']}_#{hb['i']}_#{s}", "S",
                   ha["a"][s], hb["b"][(s + SHIFT) % NS], op]
      end
    end
  end
end
HS.each do |ha|
  HS.each do |hb|
    OPS.each_with_index do |op, k|
      NS.times do |s|
        # C2 one-level composition: op(op(x,x'), op(x,x'))
        PROBES << ["C#{k}_#{ha['i']}_#{hb['i']}_#{s}", "C",
                   ha["a"][s], hb["b"][s], op]
      end
    end
  end
end
$stdout.sync = true
i = START
while i < PROBES.size
  pid, mode, da, db, op = PROBES[i]
  begin
    y = pair(da, db, op)
    if mode == "C"
      # ruling B/C: a composed probe whose OPERAND declined is not run,
      # and the position is excluded.  RAISEOP names that case so the
      # count is visible instead of inferred.
      begin
        r = compose(y, op)
        puts "#{pid}|ANSWER|#{ser(r)}"
      rescue SyntaxError
        puts "#{pid}|REFUSE|SyntaxError"
      rescue Exception => e
        puts "#{pid}|RAISE|#{e.class}"
      end
    else
      puts "#{pid}|ANSWER|#{ser(y)}"
    end
  rescue SyntaxError
    puts "#{pid}|#{mode == 'C' ? 'REFUSEOP' : 'REFUSE'}|SyntaxError"
  rescue Exception => e
    puts "#{pid}|#{mode == 'C' ? 'RAISEOP' : 'RAISE'}|#{e.class}"
  end
  i += 1
end
puts "__END__"
"""

RUBY_RUNNER = r"""
import json
import os
import queue
import subprocess
import sys
import threading
import time

ROOT = sys.argv[1]
T = json.load(open(os.path.join(ROOT, "table.json")))
OUT = T["out"]
STALL = 10.0          # seconds of silence before a probe is called stuck

HS, OPS, NS = T["holders"], T["ops"], T["n_samples"]
ids = []
for tag in ("S", "C"):
    for ha in HS:
        for hb in HS:
            for k, op in enumerate(OPS):
                for s in range(NS):
                    ids.append("%s%d_%d_%d_%d"
                               % (tag, k, ha["i"], hb["i"], s))
pos = dict((p, k) for k, p in enumerate(ids))
print("interval ruling C ruby: %d numeric holders, %d operations, %d "
      "ordered pairs, %d samples per side, 2 variants -> %d probes IN "
      "ONE PROCESS" % (len(HS), len(OPS), len(HS) ** 2, NS, len(ids)))
sys.stdout.flush()


def pump(fh, q):
    for line in fh:
        q.put(line.rstrip("\n"))
    q.put(None)


got = {}
start = 0
restarts = 0
stall_s = 0.0
t0 = time.time()
while start < len(ids) and restarts < 600:
    pr = subprocess.Popen(["ruby", os.path.join(ROOT, "drv.rb"), ROOT,
                           str(start)],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, text=True, bufsize=1)
    q = queue.Queue()
    threading.Thread(target=pump, args=(pr.stdout, q), daemon=True).start()
    last = start - 1
    ended = stalled = False
    while True:
        try:
            line = q.get(timeout=STALL)
        except queue.Empty:
            stalled = True
            stall_s += STALL
            break
        if line is None:
            break
        if line == "__END__":
            ended = True
            continue
        if "|" not in line:
            continue
        pid = line.split("|", 1)[0]
        k = pos.get(pid)
        if k is None:
            continue
        got[pid] = line
        if k > last:
            last = k
    if stalled:
        try:
            pr.kill()          # the subprocess API's own name; the
                               # OUTCOME this produces is ABORT
        except OSError:
            pass
    pr.wait()
    if ended or last >= len(ids) - 1:
        break
    nxt = last + 1
    why = ("stalled>%.0fs" % STALL) if stalled else ("rc%s" % pr.returncode)
    got[ids[nxt]] = "%s|ABORT|%s" % (ids[nxt], why)
    start = nxt + 1
    restarts += 1
    print("[restart %d] %s stopped the process (%s); continuing at "
          "%d/%d after %.1f s"
          % (restarts, ids[nxt], why, start, len(ids), time.time() - t0))
    sys.stdout.flush()

el = time.time() - t0
ans = raises = aborts = refused = missing = op_declines = 0
with open(OUT, "w") as f:
    for pid in ids:
        line = got.get(pid, "%s|MISSING|" % pid)
        f.write(line + "\n")
        kind = line.split("|")[1]
        if kind == "ANSWER":
            ans += 1
        elif kind == "RAISE":
            raises += 1
        elif kind in ("RAISEOP", "REFUSEOP"):
            op_declines += 1
        elif kind == "ABORT":
            aborts += 1
        elif kind == "REFUSE":
            refused += 1
        else:
            missing += 1
    f.write("__SUMMARY__|ruby|%d|%d|%d|%d|%d|%.3f\n"
            % (len(ids), ans, raises, aborts, refused, el))
    f.write("__TIMING__|ruby|processes=%d|probes=%d|"
            "compile_invocations=0|compile_s=0.000|"
            "stall_budget_s=%.3f|evaluate_s=%.3f|total_s=%.3f|restarts=%d|"
            "operand_declines=%d\n"
            % (restarts + 1, len(ids), stall_s, el - stall_s, el,
               restarts, op_declines))
print("== interval ruling C ruby: %d probes, %d answers, %d raises, "
      "%d operand-declines (composed probe NOT run), %d aborts, "
      "%d refusals, %d missing, %d restarts, %.2f s"
      % (len(ids), ans, raises, op_declines, aborts, refused, missing,
         restarts, el))
print("== TIMING ruby: 0 files compiled (route C is eval, nothing is "
      "compiled); %d ruby process(es) -- 1 plus %d restarts past a probe "
      "that stopped it; wall %.2f s of which %.2f s is the %.0f s "
      "inactivity budget spent on stalls and %.2f s is actual evaluation"
      % (restarts + 1, restarts, el, stall_s, STALL, el - stall_s))
"""


def emit_ruby(smoke=False):
    tab = G.numeric_table("ruby")
    op_list = ops("ruby")
    if smoke:
        tab = tab[:2]
    out = "/out/iv_ruby_c_smoke.txt" if smoke else "/out/iv_ruby_c0.txt"
    payload = dict(language="ruby", ops=op_list, n_samples=N,
                   holders=tab, shift=SHIFT, out=out)
    ncell = len(tab) ** 2 * len(op_list)
    nprobe = ncell * N * 2
    sh = (RUBY_SH
          .replace("__TABLE__", wrap(b64gz(json.dumps(payload))))
          .replace("__DRIVER__", wrap(base64.b64encode(
              RUBY_DRIVER.encode("utf-8")).decode("ascii")))
          .replace("__RUNNER__", RUBY_RUNNER)
          .replace("__NP__", str(nprobe)))
    name = "iv_ruby_c_smoke.sh" if smoke else "iv_ruby_c0.sh"
    if smoke:
        sh = sh.replace("iv_ruby_c0", "iv_ruby_c_smoke")
    return name, sh, ncell, nprobe


# ------------------------------------------------------------------

def main():
    smoke = "--smoke" in sys.argv
    os.makedirs(LANES, exist_ok=True)
    print("interval ruling-C lanes -- break the diagonal.  C1 SHIFTED "
          "(x_k OP x_{(k+%d) mod %d}) and C2 ONE-LEVEL COMPOSITION "
          "(op(op(x,x'), op(x,x'))).  Pilot scope: rust + ruby only.%s"
          % (SHIFT, N, "  SMOKE." if smoke else ""))

    name, sh, nshift, ncomp, skipped, nprobe = emit_rust(smoke)
    print("  rust: %d accepted numeric cells get a SHIFTED row; %d of "
          "them also get a COMPOSED row" % (nshift, ncomp))
    for why, n in skipped.most_common():
        print("        %d cells composed NOT emitted -- %s" % (n, why))
    print("  %-18s %7d probes, %d chunk files at %d probes each, %d KB"
          % (name, nprobe, (nprobe + CHUNK - 1) // CHUNK, CHUNK,
             len(sh) // 1024))
    write(name, sh)

    name, sh, ncell, nprobe = emit_ruby(smoke)
    print("  ruby: %d cells x %d samples x 2 variants = %d probes in ONE "
          "process" % (ncell, N, nprobe))
    print("  %-18s %7d probes, 0 chunk files (route C compiles nothing), "
          "%d KB" % (name, nprobe, len(sh) // 1024))
    write(name, sh)


def write(name, sh):
    p = os.path.join(LANES, name)
    with open(p, "w") as f:
        f.write(sh)
    os.chmod(p, 0o755)
    if os.path.isdir(DROP):
        with open(os.path.join(DROP, name), "w") as f:
            f.write(sh)
        print("      dropped -> %s" % os.path.join(DROP, name))


if __name__ == "__main__":
    main()
