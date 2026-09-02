#!/usr/bin/env python3
"""l3_routec.py -- ROUTE C lanes for the open-dispatch three.

CORE_0_3_2 ruling 5, route C: for python, ruby and php, where `+`
resolves at RUN time through an `__add__`-style slot, execution is the
ONLY acceptance evidence that exists -- log_026 finding 2.  These three
therefore get the full thing here: full ordered holder pairs (ruling 2)
x the language's operator menu x the FULL VALUE MATRIX (ruling 3).

Each lane carries a small table (holders, their per-value-class
declarations, the operator menu) and ASSEMBLES the probes inside the
container, so the payload stays small while the probe count stays full.

Every result row is (operation, form, holder, value class) -> verdict
or answer, which is the shape CORE_0_3_2 phase 3 asks for.
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
from l3_accept import holders, ops                       # noqa: E402

LANGS = ["python", "ruby", "php"]


def table(lang):
    hs, _ = holders(lang)
    return dict(language=lang, ops=ops(lang),
                holders=[dict(form=h["form"], rep=h["rep"],
                              pre=h.get("pre", ""), values=h["values"])
                         for h in hs])


PY_DRIVER = r'''
import json, os, re, signal, sys, time, traceback

T = json.load(open(os.path.join(ROOT, "table.json")))
HS, OPS = T["holders"], T["ops"]
OUT = open("/out/rc_python.txt", "w")

def hms(x):
    if x is None or x < 0: return "--:--:--"
    x = int(x); return "%02d:%02d:%02d" % (x//3600, (x%3600)//60, x%60)

total = 0
for i, ha in enumerate(HS):
    for j, hb in enumerate(HS):
        total += len(ha["values"]) * len(hb["values"]) * len(OPS)
print("ROUTE C python: %d holders, %d operations, %d ordered pairs, "
      "%d probes (full value matrix)"
      % (len(HS), len(OPS), len(HS)**2, total))
sys.stdout.flush()

# CAP THE ADDRESS SPACE.  Some probes are unbounded ALLOCATIONS, not
# slow loops -- a sequence holder times a whole-number holder carrying
# the i64max value class asks for a list of 9.2e18 elements.  The 2 s
# signal budget below cannot stop that: the allocation never returns to
# the interpreter loop, so the kernel OOM-kills the process first.
# Measured 2026-08-18: the first run was SIGKILLed after 19829 of
# 342225 probes and the lane still exited 0.  With a cap the same probe
# raises MemoryError, which is a RECORDABLE answer, and the run
# continues.
import resource
_CAP = 1 << 30
try:
    resource.setrlimit(resource.RLIMIT_AS, (_CAP, _CAP))
    print("address space capped at %d MiB; unbounded allocations now "
          "raise MemoryError instead of killing the run" % (_CAP >> 20))
except Exception as e:
    print("WARNING: could not cap address space: %r" % (e,))
sys.stdout.flush()


class Budget(Exception):
    pass

def _alarm(sig, frm):
    raise Budget()
signal.signal(signal.SIGALRM, _alarm)

def rn(s, n):
    return re.sub(r"\bv\b", n, s)

pre = set()
for h in HS:
    for line in (h.get("pre") or "").splitlines():
        if line.strip():
            pre.add(line.strip())
BASE = {}
for line in sorted(pre):
    try:
        exec(line, BASE)
    except Exception:
        pass

t0 = time.time(); done = 0
ans = raises = refused = budget = 0
for i, ha in enumerate(HS):
    for j, hb in enumerate(HS):
        for vca, da in sorted(ha["values"].items()):
            for vcb, db in sorted(hb["values"].items()):
                src_head = rn(da, "a") + "\n" + rn(db, "b") + "\n"
                for op in OPS:
                    pid = "P%d_%d_%s_%s_%s" % (i, j, vca, vcb, op)
                    src = src_head + "__r = (a) %s (b)\n" % op
                    try:
                        code = compile(src, "<probe>", "exec")
                    except SyntaxError as e:
                        OUT.write("%s|REFUSE|%s\n" % (pid, type(e).__name__))
                        refused += 1; done += 1; continue
                    ns = dict(BASE)
                    signal.setitimer(signal.ITIMER_REAL, 2.0)
                    try:
                        exec(code, ns)
                        r = ns.get("__r")
                        OUT.write("%s|ANSWER|%s:%s\n"
                                  % (pid, type(r).__name__, repr(r)[:120]))
                        ans += 1
                    except Budget:
                        OUT.write("%s|BUDGET|2s\n" % pid); budget += 1
                    except BaseException as e:
                        OUT.write("%s|RAISE|%s\n" % (pid, type(e).__name__))
                        raises += 1
                    finally:
                        signal.setitimer(signal.ITIMER_REAL, 0)
                    done += 1
                    if done % 20000 == 0:
                        el = time.time() - t0
                        print("[progress] python [%d/%d] %5.1f%%  elapsed %s"
                              "  ETA %s  mean %.2f ms"
                              % (done, total, 100.0*done/total, hms(el),
                                 hms(el/done*(total-done)), 1000.0*el/done))
                        sys.stdout.flush()
el = time.time() - t0
print("== python route C: %d probes, %d answers, %d raises, %d refusals, "
      "%d budget, %.1f s" % (done, ans, raises, refused, budget, el))
OUT.write("__SUMMARY__|%d|%d|%d|%d|%d|%.3f\n"
          % (done, ans, raises, refused, budget, el))
OUT.close()
'''

RUBY_DRIVER = r'''
require 'json'
T = JSON.parse(File.read(File.join(ROOT, "table.json")))
HS = T["holders"]; OPS = T["ops"]
OUT = File.open("/out/rc_ruby.txt", "w")
def hms(x); x = x.to_i; format("%02d:%02d:%02d", x/3600, (x%3600)/60, x%60); end
total = 0
HS.each { |a| HS.each { |b| total += a["values"].size * b["values"].size * OPS.size } }
puts "ROUTE C ruby: #{HS.size} holders, #{OPS.size} operations, "\
     "#{HS.size**2} ordered pairs, #{total} probes (full value matrix)"
$stdout.flush
t0 = Time.now; done = 0; ans = 0; raises = 0; refused = 0
HS.each_with_index do |ha, i|
  HS.each_with_index do |hb, j|
    ha["values"].sort.each do |vca, da|
      hb["values"].sort.each do |vcb, db|
        head = da.gsub(/\bv\b/, "a") + "\n" + db.gsub(/\bv\b/, "b") + "\n"
        OPS.each do |op|
          pid = "P#{i}_#{j}_#{vca}_#{vcb}_#{op}"
          src = head + "__r = (a) #{op} (b)\n__r"
          begin
            r = eval(src)
            OUT.puts "#{pid}|ANSWER|#{r.class}:#{r.inspect[0,120]}"
            ans += 1
          rescue SyntaxError => e
            OUT.puts "#{pid}|REFUSE|SyntaxError"; refused += 1
          rescue Exception => e
            OUT.puts "#{pid}|RAISE|#{e.class}"; raises += 1
          end
          done += 1
          if done % 20000 == 0
            el = Time.now - t0
            puts "[progress] ruby [#{done}/#{total}] "\
                 "#{(100.0*done/total).round(1)}%  elapsed #{hms(el)}"\
                 "  ETA #{hms(el/done*(total-done))}"\
                 "  mean #{(1000.0*el/done).round(2)} ms"
            $stdout.flush
          end
        end
      end
    end
  end
end
el = Time.now - t0
puts "== ruby route C: #{done} probes, #{ans} answers, #{raises} raises, "\
     "#{refused} refusals, #{el.round(1)} s"
OUT.puts "__SUMMARY__|#{done}|#{ans}|#{raises}|#{refused}|0|#{el.round(3)}"
OUT.close
'''

PHP_DRIVER = r'''<?php
$T = json_decode(file_get_contents($ROOT . "/table.json"), true);
$HS = $T["holders"]; $OPS = $T["ops"];
$OUT = fopen("/out/rc_php.txt", "w");
function hms($x) { $x = (int)$x;
  return sprintf("%02d:%02d:%02d", intdiv($x,3600), intdiv($x%3600,60), $x%60); }

// HOIST class declarations out of the per-probe eval.  A holder loader
// that declares a class ("class R0 {}") is eval'd once per probe, and
// the SECOND eval is a "Cannot redeclare class" FATAL -- uncatchable,
// it kills the process.  Measured 2026-08-18: the first run died after
// 2001 of 215306 probes and still exited 0.  Each distinct declaration
// is now eval'd exactly once here and stripped from the probe source.
$SEEN = [];
foreach ($HS as $i => $h) {
  foreach ($h["values"] as $vc => $src) {
    $rest = preg_replace_callback(
      '/^\s*(?:final\s+|abstract\s+)?class\s+\w+[^{]*\{.*?\}\s*$/ms',
      function ($m) use (&$SEEN) {
        $d = trim($m[0]);
        if (!isset($SEEN[$d])) { $SEEN[$d] = 1; eval($d); }
        return "";
      }, $src);
    $HS[$i]["values"][$vc] = $rest;
  }
}
echo "hoisted " . count($SEEN) . " class declaration(s) out of the "
   . "per-probe eval\n";

$total = 0;
foreach ($HS as $a) foreach ($HS as $b)
  $total += count($a["values"]) * count($b["values"]) * count($OPS);
echo "ROUTE C php: " . count($HS) . " holders, " . count($OPS)
   . " operations, " . (count($HS)**2) . " ordered pairs, $total probes"
   . " (full value matrix)\n";
$t0 = microtime(true); $done = 0; $ans = 0; $raises = 0; $refused = 0;
foreach ($HS as $i => $ha) {
 foreach ($HS as $j => $hb) {
  $va = $ha["values"]; ksort($va);
  $vb = $hb["values"]; ksort($vb);
  foreach ($va as $vca => $da) {
   foreach ($vb as $vcb => $db) {
    $head = preg_replace('/\$v\b/', '$a', $da) . ";\n"
          . preg_replace('/\$v\b/', '$b', $db) . ";\n";
    foreach ($OPS as $op) {
     $pid = "P{$i}_{$j}_{$vca}_{$vcb}_{$op}";
     $src = $head . "\$__r = (\$a) $op (\$b);";
     try {
       $r = null; $__r = null;
       eval($src);
       $t = gettype($__r);
       $s = is_scalar($__r) ? (string)$__r : json_encode($__r);
       fwrite($OUT, "$pid|ANSWER|$t:" . substr((string)$s, 0, 120) . "\n");
       $ans++;
     } catch (ParseError $e) {
       fwrite($OUT, "$pid|REFUSE|ParseError\n"); $refused++;
     } catch (Throwable $e) {
       fwrite($OUT, "$pid|RAISE|" . get_class($e) . "\n"); $raises++;
     }
     $done++;
     if ($done % 20000 === 0) {
       $el = microtime(true) - $t0;
       printf("[progress] php [%d/%d] %5.1f%%  elapsed %s  ETA %s"
              . "  mean %.2f ms\n", $done, $total, 100.0*$done/$total,
              hms($el), hms($el/$done*($total-$done)), 1000.0*$el/$done);
       flush();
     }
    }
   }
  }
 }
}
$el = microtime(true) - $t0;
echo "== php route C: $done probes, $ans answers, $raises raises, "
   . "$refused refusals, " . round($el,1) . " s\n";
fwrite($OUT, "__SUMMARY__|$done|$ans|$raises|$refused|0|" . round($el,3) . "\n");
fclose($OUT);
'''


def emit(lang):
    t = table(lang)
    raw = json.dumps(t).encode()
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as g:
        g.write(raw)
    b = base64.b64encode(buf.getvalue()).decode()
    b = "\n".join(b[i:i+76] for i in range(0, len(b), 76))
    n_pairs = len(t["holders"]) ** 2
    body = {"python": PY_DRIVER, "ruby": RUBY_DRIVER, "php": PHP_DRIVER}[lang]
    # the driver goes to a FILE, base64-carried like the table, so no
    # shell expansion can reach inside it.
    dext, dcmd = {"python": ("py", "python3"), "ruby": ("rb", "ruby"),
                  "php": ("php", "php")}[lang]
    root = "/work/rc_" + lang
    if lang == "python":
        body = ('import sys\nROOT = sys.argv[1]\n' + body)
    elif lang == "ruby":
        body = ('ROOT = ARGV[0]\n' + body)
    else:
        body = body.replace("<?php\n", "<?php\n$ROOT = $argv[1];\n")
    db = base64.b64encode(body.encode()).decode()
    db = "\n".join(db[i:i+76] for i in range(0, len(db), 76))
    run = ("base64 -d <<'DRV_EOF' > \"$ROOT/drv.%s\"\n%s\nDRV_EOF\n"
           "%s \"$ROOT/drv.%s\" \"$ROOT\"\n" % (dext, db, dcmd, dext))
    sh = ("#!/bin/sh\n"
          "# layer-3 phase 3 ROUTE C lane -- %s -- generated by l3_routec.py\n"
          "# Execution is the ONLY acceptance evidence for this language\n"
          "# (CORE_0_3_2 ruling 5 route C; log_026 finding 2).\n"
          "# FULL ordered pairs (%d) x FULL value matrix x operator menu.\n"
          "set -u\nexport HOME=/work\n"
          "ROOT=/work/rc_%s\nrm -rf \"$ROOT\"; mkdir -p \"$ROOT\"\n"
          "echo \"=== layer-3 route C -- %s ===\"\n"
          "date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ\n"
          "base64 -d <<'B64_EOF' | gunzip > \"$ROOT/table.json\"\n%s\nB64_EOF\n"
          "%s"
          "echo \"=== route C %s done ===\"\n"
          "date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ\n"
          % (lang, n_pairs, lang, lang, b, run, lang))
    p = os.path.join(LANES, "rc_%s.sh" % lang)
    open(p, "w").write(sh)
    os.chmod(p, 0o755)
    print("wrote %s (%d holders, %d ops, %d ordered pairs, %.1f KB)"
          % (p, len(t["holders"]), len(t["ops"]), n_pairs,
             os.path.getsize(p) / 1024.0))


if __name__ == "__main__":
    for lang in (sys.argv[1:] or LANGS):
        emit(lang)
