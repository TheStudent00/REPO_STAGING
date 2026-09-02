#!/usr/bin/env python3
"""l3_construct.py -- layer-3 CONSTRUCT lanes.

Design of record: construct_design.md (2026-08-19), which is the owner's
blessed access / flow / binding families with the SCAFFOLD principle,
the slot discipline carried over from the operator pass, and the TRACE
as the observation standard for flow.

This file builds, per language:

  manifest_construct_<lang>.json   frozen before the run; the holder
                                   list in POSITION order, the value
                                   classes per holder, the construct
                                   list, the scaffold per construct.
                                   Decision 14 -- positional ids are
                                   unreadable without it (log 029).
  lanes/kc_<lang>.sh               route-C languages: one lane, it is
                                   both acceptance and answers.

The lane carries a small table and ASSEMBLES the probes inside the
container, so the payload stays small while the probe count stays full.
That is the same shape l3_routec.py used for the operator pass.
"""

import base64
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.join(HERE, "lanes")
os.makedirs(LANES, exist_ok=True)
sys.path.insert(0, HERE)
from l3_accept import holders                          # noqa: E402
from construct_space import space, AUG_OPS, JUMP_K     # noqa: E402

ROUTE_C = ["python", "ruby", "php"]


def cat():
    return json.load(open(os.path.join(HERE, "construct_catalogue.json")))


def manifest(lang):
    hs, _ = holders(lang)
    sp = space(lang)
    c = cat()[lang]
    m = dict(
        language=lang,
        frozen="2026-08-19",
        design="construct_design.md",
        holders=[dict(i=n, form=h["form"], rep=h["rep"],
                      value_classes=sorted(h["values"]))
                 for n, h in enumerate(hs)],
        constructs={r["construct"]: dict(
            present=r["present"],
            grammar_kind=(c[r["construct"].split(".")[0]]
                           [r["construct"].split(".")[1]]["kind"]),
            acceptance_probes=r["acceptance"],
            answer_probes=r["answers"]) for r in sp["constructs"]},
        aug_ops=AUG_OPS,
        jump_k=JUMP_K,
        totals=dict(acceptance=sp["acceptance_probes"],
                    answers=sp["answer_probes"]),
    )
    p = os.path.join(HERE, "manifest_construct_%s.json" % lang)
    json.dump(m, open(p, "w"), indent=1)
    return m


def table(lang):
    hs, _ = holders(lang)
    sp = space(lang)
    return dict(language=lang,
                holders=[dict(form=h["form"], rep=h["rep"],
                              pre=h.get("pre", ""), values=h["values"])
                         for h in hs],
                constructs=[r["construct"] for r in sp["constructs"]
                            if r["present"]],
                aug_ops=AUG_OPS, jump_k=JUMP_K)


# ------------------------------------------------------------------
# the python driver.  It is the proof language: no compile step, so a
# refusal isolates to its exact probe and the whole loop is one process.
# ------------------------------------------------------------------
PY_DRIVER = r'''
import json, os, re, signal, struct, sys, time

T = json.load(open(os.path.join(ROOT, "table.json")))
HS = T["holders"]
CONS = T["constructs"]
AUG = T["aug_ops"]
KMAX = T["jump_k"]
OUT = open("/out/kc_python.txt", "w")
CAPSTEPS = 8

import resource
_CAP = 1 << 30
try:
    resource.setrlimit(resource.RLIMIT_AS, (_CAP, _CAP))
except Exception:
    pass


def hms(x):
    if x is None or x < 0: return "--:--:--"
    x = int(x); return "%02d:%02d:%02d" % (x//3600, (x%3600)//60, x%60)


# ---- the answers_encoding.md encoder ----------------------------
def enc(v, depth=0):
    if depth > 3:
        return "OPAQUE:" + repr(v)[:40].encode("utf-8").hex()
    if v is None:
        return "NULL"
    if v is True:
        return "BOOL:true"
    if v is False:
        return "BOOL:false"
    if isinstance(v, int):
        if -(1 << 63) <= v < (1 << 63):
            return "INT:64:%016x" % (v & ((1 << 64) - 1))
        s = "-" if v < 0 else "+"
        return "BIGINT:%s%x" % (s, abs(v))
    if isinstance(v, float):
        return "FLOAT:64:%016x" % struct.unpack("<Q", struct.pack("<d", v))[0]
    if isinstance(v, str):
        b = v.encode("utf-8", "surrogatepass")
        return "STR:%d:%d:%s" % (len(v), len(b), b[:64].hex())
    if isinstance(v, bytes):
        return "STR:%d:%d:%s" % (len(v), len(v), v[:64].hex())
    if isinstance(v, tuple):
        xs = [enc(x, depth+1) for x in v[:8]]
        return "TUP:%d[%s]" % (len(v), ",".join(xs))
    if isinstance(v, (list, set, frozenset)):
        xs = [enc(x, depth+1) for x in list(v)[:8]]
        return "LIST:%d[%s]" % (len(v), ",".join(xs))
    if isinstance(v, dict):
        xs = sorted("%s=>%s" % (enc(k, depth+1), enc(w, depth+1))
                    for k, w in list(v.items())[:8])
        return "MAP:%d[%s]" % (len(v), ",".join(xs))
    return "OPAQUE:" + repr(v)[:40].encode("utf-8").hex()


def tname(v):
    return type(v).__name__


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
BASE["__enc"] = enc
BASE["__CAP"] = CAPSTEPS

# ---- the scaffolds.  fixed, minimal, inert (decision 4).  the only
# thing that changes between two probes of one construct is what goes
# into {A}, {B}, {K}.
SCAF = {
 "access.subscript": "__r = (a)[(b)]\n",
 "access.slice":     "__r = (a)[(b):(c)]\n",
 "access.member":    "__r = (a).f\n",
 "flow.if":          "if (a):\n    __t.append('BR=then')\n"
                     "else:\n    __t.append('BR=else')\n",
 "flow.for":         "__n = 0\nfor __v in (a):\n"
                     "    __t.append('IT=' + __enc(__v))\n"
                     "    __n += 1\n"
                     "    if __n >= __CAP:\n"
                     "        __t.append('STOP=%d' % __n)\n        break\n",
 "flow.while":       "__n = 0\nwhile (a):\n"
                     "    __t.append('IT=' + __enc(__n))\n"
                     "    __n += 1\n"
                     "    if __n >= __CAP:\n"
                     "        __t.append('STOP=%d' % __n)\n        break\n",
 "flow.try":         "try:\n    __t.append('BR=try')\n    __z = (a)[0]\n"
                     "except BaseException as __e:\n"
                     "    __t.append('BR=catch')\n"
                     "    __t.append('THROW=' + type(__e).__name__)\n"
                     "finally:\n    __t.append('BR=finally')\n",
 "flow.break":       "for __v in [1, 2, 3, 4, 5]:\n"
                     "    if __v == {K}:\n"
                     "        __t.append('STOP=%d' % (__v - 1))\n        break\n"
                     "    __t.append('IT=' + __enc(__v))\n",
 "flow.continue":    "for __v in [1, 2, 3, 4, 5]:\n"
                     "    if __v == {K}:\n"
                     "        __t.append('SKIP=%d' % __v)\n        continue\n"
                     "    __t.append('IT=' + __enc(__v))\n",
 "binding.assign":   "__x = (a)\n__t.append('BIND=' + __enc(__x))\n",
 "binding.augassign": "__x = (a)\n__x {OP} (b)\n"
                      "__t.append('BIND=' + __enc(__x))\n",
 "binding.unpack":   "__p, __q = (a)\n__t.append('BIND=' + __enc(__p))\n"
                     "__t.append('BIND=' + __enc(__q))\n",
}
TRACE_CONS = set(k for k in SCAF if k.startswith(("flow.", "binding.")))


def whole_holder():
    for n, h in enumerate(HS):
        if h["form"] == "whole":
            return n, h
    return None, None

WI, WH = whole_holder()
BOUNDS = sorted(WH["values"])[:6] if WH else []

# ---- the SIZE, printed before anything runs -----------------------
V = sum(len(h["values"]) for h in HS)
M = sum(len(a["values"]) * len(b["values"]) for a in HS for b in HS)
total = 0
for c in CONS:
    if c in ("flow.break", "flow.continue"):
        total += KMAX
    elif c == "access.subscript":
        total += M
    elif c == "binding.augassign":
        total += M * len(AUG)
    elif c == "access.slice":
        total += V * len(BOUNDS) * len(BOUNDS)
    else:
        total += V
print("CONSTRUCTS python: %d holders, %d values, %d constructs, "
      "%d probes" % (len(HS), V, len(CONS), total))
sys.stdout.flush()

t0 = time.time(); done = 0
ans = tr = raises = refused = budget = 0


def emit(pid, src, kind):
    """run one probe.  kind is 'answer' or 'trace'."""
    global done, ans, tr, raises, refused, budget
    done += 1
    try:
        code = compile(src, "<probe>", "exec")
    except SyntaxError as e:
        OUT.write("%s|-|REFUSE:%s\n" % (pid, type(e).__name__))
        refused += 1
        return
    ns = dict(BASE)
    ns["__t"] = []
    signal.setitimer(signal.ITIMER_REAL, 2.0)
    try:
        exec(code, ns)
        if kind == "answer":
            r = ns.get("__r")
            OUT.write("%s|%s|%s\n" % (pid, tname(r), enc(r)))
            ans += 1
        else:
            steps = ns["__t"]
            ty = "-"
            its = [s for s in steps if s.startswith("IT=")
                   or s.startswith("BIND=")]
            OUT.write("%s|%s|TRACE:%d[%s]\n"
                      % (pid, ty, len(steps), ",".join(steps)))
            tr += 1
    except Budget:
        OUT.write("%s|-|BUDGET:2s\n" % pid); budget += 1
    except BaseException as e:
        OUT.write("%s|-|RAISE:%s\n" % (pid, type(e).__name__))
        raises += 1
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
    if done % 5000 == 0:
        el = time.time() - t0
        print("[progress] python constructs [%d/%d] %5.1f%%  elapsed %s"
              "  ETA %s  mean %.2f ms"
              % (done, total, 100.0*done/total, hms(el),
                 hms(el/done*(total-done)), 1000.0*el/done))
        sys.stdout.flush()


for c in CONS:
    sc = SCAF[c]
    if c in ("flow.break", "flow.continue"):
        for k in range(1, KMAX + 1):
            emit("K%s_%d" % (c, k), sc.replace("{K}", str(k)), "trace")
        continue
    if c == "access.subscript":
        for i, ha in enumerate(HS):
            for j, hb in enumerate(HS):
                for vca, da in sorted(ha["values"].items()):
                    for vcb, db in sorted(hb["values"].items()):
                        src = rn(da, "a") + "\n" + rn(db, "b") + "\n" + sc
                        emit("K%s_%d_%d_%s_%s" % (c, i, j, vca, vcb),
                             src, "answer")
        continue
    if c == "binding.augassign":
        for i, ha in enumerate(HS):
            for j, hb in enumerate(HS):
                for vca, da in sorted(ha["values"].items()):
                    for vcb, db in sorted(hb["values"].items()):
                        head = rn(da, "a") + "\n" + rn(db, "b") + "\n"
                        for op in AUG:
                            emit("K%s%s_%d_%d_%s_%s"
                                 % (c, op, i, j, vca, vcb),
                                 head + sc.replace("{OP}", op), "trace")
        continue
    if c == "access.slice":
        for i, ha in enumerate(HS):
            for vca, da in sorted(ha["values"].items()):
                for b1 in BOUNDS:
                    for b2 in BOUNDS:
                        src = (rn(da, "a") + "\n"
                               + rn(WH["values"][b1], "b") + "\n"
                               + rn(WH["values"][b2], "c") + "\n" + sc)
                        emit("K%s_%d_%s_%s_%s" % (c, i, vca, b1, b2),
                             src, "answer")
        continue
    kind = "trace" if c in TRACE_CONS else "answer"
    for i, ha in enumerate(HS):
        for vca, da in sorted(ha["values"].items()):
            emit("K%s_%d_%s" % (c, i, vca), rn(da, "a") + "\n" + sc, kind)

el = time.time() - t0
print("== python constructs: %d probes, %d answers, %d traces, %d raises, "
      "%d refusals, %d budget, %.1f s"
      % (done, ans, tr, raises, refused, budget, el))
OUT.write("__SUMMARY__|%d|%d|%d|%d|%d|%d|%.3f\n"
          % (done, ans, tr, raises, refused, budget, el))
OUT.close()
'''


# ------------------------------------------------------------------
# ruby.  Route C, same as python: execution is the only acceptance
# evidence.  The scaffolds are ruby's own spellings of the same twelve
# roles; ruby has no slice syntax (catalogue: access.slice ABSENT) so
# that construct is simply not generated.
# ------------------------------------------------------------------
RB_DRIVER = r'''
require 'json'
require 'set'
ROOT = ARGV[0]
T = JSON.parse(File.read(File.join(ROOT, "table.json")))
HS = T["holders"]
CONS = T["constructs"]
AUG = T["aug_ops"]
KMAX = T["jump_k"]
OUT = File.open("/out/kc_ruby.txt", "w")
CAPSTEPS = 8

def hms(x)
  return "--:--:--" if x.nil? || x < 0
  x = x.to_i
  format("%02d:%02d:%02d", x / 3600, (x % 3600) / 60, x % 60)
end

def enc(v, depth = 0)
  return "OPAQUE:" + v.inspect[0, 40].unpack1("H*") if depth > 3
  case v
  when nil then "NULL"
  when true then "BOOL:true"
  when false then "BOOL:false"
  when Integer
    if v >= -(2**63) && v < 2**63
      format("INT:64:%016x", v & (2**64 - 1))
    else
      format("BIGINT:%s%x", v.negative? ? "-" : "+", v.abs)
    end
  when Float
    format("FLOAT:64:%016x", [v].pack("E").unpack1("Q<"))
  when String
    b = v.dup.force_encoding("BINARY")
    format("STR:%d:%d:%s", (v.valid_encoding? ? v.length : v.bytesize),
           v.bytesize, b[0, 64].unpack1("H*"))
  when Symbol then enc(v.to_s, depth + 1)
  when Array
    "LIST:%d[%s]" % [v.length, v[0, 8].map { |x| enc(x, depth + 1) }.join(",")]
  when Hash
    xs = v.first(8).map { |k, w| enc(k, depth + 1) + "=>" + enc(w, depth + 1) }
    "MAP:%d[%s]" % [v.length, xs.sort.join(",")]
  else
    "OPAQUE:" + v.inspect[0, 40].unpack1("H*")
  end
end

SCAF = {
 "access.subscript"  => "__r = (a)[(b)]\n",
 "access.member"     => "__r = (a).f\n",
 "flow.if"           => "if (a)\n  __t << 'BR=then'\nelse\n  __t << 'BR=else'\nend\n",
 "flow.for"          => "__n = 0\nfor __v in (a)\n  __t << ('IT=' + enc(__v))\n" \
                        "  __n += 1\n  if __n >= 8\n    __t << \"STOP=\#{__n}\"\n    break\n  end\nend\n",
 "flow.while"        => "__n = 0\nwhile (a)\n  __t << ('IT=' + enc(__n))\n" \
                        "  __n += 1\n  if __n >= 8\n    __t << \"STOP=\#{__n}\"\n    break\n  end\nend\n",
 "flow.try"          => "begin\n  __t << 'BR=try'\n  __z = (a)[0]\n" \
                        "rescue Exception => __e\n  __t << 'BR=catch'\n" \
                        "  __t << ('THROW=' + __e.class.name)\nensure\n  __t << 'BR=finally'\nend\n",
 "flow.break"        => "for __v in [1, 2, 3, 4, 5]\n  if __v == {K}\n" \
                        "    __t << \"STOP=\#{__v - 1}\"\n    break\n  end\n" \
                        "  __t << ('IT=' + enc(__v))\nend\n",
 "flow.continue"     => "for __v in [1, 2, 3, 4, 5]\n  if __v == {K}\n" \
                        "    __t << \"SKIP=\#{__v}\"\n    next\n  end\n" \
                        "  __t << ('IT=' + enc(__v))\nend\n",
 "binding.assign"    => "__x = (a)\n__t << ('BIND=' + enc(__x))\n",
 "binding.augassign" => "__x = (a)\n__x {OP} (b)\n__t << ('BIND=' + enc(__x))\n",
 "binding.unpack"    => "__p, __q = (a)\n__t << ('BIND=' + enc(__p))\n__t << ('BIND=' + enc(__q))\n",
}
TRACE_CONS = SCAF.keys.select { |k| k.start_with?("flow.", "binding.") }.to_set

def rn(s, n)
  s.gsub(/\bv\b/, n)
end

PRE = []
HS.each do |h|
  (h["pre"] || "").each_line { |l| PRE << l.strip unless l.strip.empty? }
end
PRE.uniq.sort.each { |l| begin; eval(l, TOPLEVEL_BINDING); rescue Exception; end }

V = HS.map { |h| h["values"].length }.sum
M = HS.sum { |a| HS.sum { |b| a["values"].length * b["values"].length } }
total = 0
CONS.each do |c|
  total += case c
           when "flow.break", "flow.continue" then KMAX
           when "access.subscript" then M
           when "binding.augassign" then M * AUG.length
           else V
           end
end
puts "CONSTRUCTS ruby: #{HS.length} holders, #{V} values, " \
     "#{CONS.length} constructs, #{total} probes"
$stdout.flush

$t0 = Time.now
$done = 0; $ans = 0; $tr = 0; $raises = 0; $refused = 0
$total = total

def emit(pid, src, kind)
  $done += 1
  __t = []
  begin
    b = binding
    r = eval(src + (kind == "answer" ? "\n__r" : "\nnil"), b)
    if kind == "answer"
      OUT.write("#{pid}|#{r.class.name}|#{enc(r)}\n"); $ans += 1
    else
      OUT.write("#{pid}|-|TRACE:#{__t.length}[#{__t.join(',')}]\n"); $tr += 1
    end
  rescue SyntaxError => e
    OUT.write("#{pid}|-|REFUSE:#{e.class.name}\n"); $refused += 1
  rescue Exception => e
    OUT.write("#{pid}|-|RAISE:#{e.class.name}\n"); $raises += 1
  end
  if $done % 5000 == 0
    el = Time.now - $t0
    puts format("[progress] ruby constructs [%d/%d] %5.1f%%  elapsed %s" \
                "  ETA %s  mean %.2f ms", $done, $total,
                100.0 * $done / $total, hms(el),
                hms(el / $done * ($total - $done)), 1000.0 * el / $done)
    $stdout.flush
  end
end

CONS.each do |c|
  sc = SCAF[c]
  next if sc.nil?
  if ["flow.break", "flow.continue"].include?(c)
    (1..KMAX).each { |k| emit("K#{c}_#{k}", sc.gsub("{K}", k.to_s), "trace") }
    next
  end
  if c == "access.subscript"
    HS.each_with_index do |ha, i|
      HS.each_with_index do |hb, j|
        ha["values"].sort.each do |vca, da|
          hb["values"].sort.each do |vcb, db|
            emit("K#{c}_#{i}_#{j}_#{vca}_#{vcb}",
                 rn(da, "a") + "\n" + rn(db, "b") + "\n" + sc, "answer")
          end
        end
      end
    end
    next
  end
  if c == "binding.augassign"
    HS.each_with_index do |ha, i|
      HS.each_with_index do |hb, j|
        ha["values"].sort.each do |vca, da|
          hb["values"].sort.each do |vcb, db|
            head = rn(da, "a") + "\n" + rn(db, "b") + "\n"
            AUG.each do |op|
              emit("K#{c}#{op}_#{i}_#{j}_#{vca}_#{vcb}",
                   head + sc.gsub("{OP}", op), "trace")
            end
          end
        end
      end
    end
    next
  end
  kind = TRACE_CONS.include?(c) ? "trace" : "answer"
  HS.each_with_index do |ha, i|
    ha["values"].sort.each do |vca, da|
      emit("K#{c}_#{i}_#{vca}", rn(da, "a") + "\n" + sc, kind)
    end
  end
end

el = Time.now - $t0
puts format("== ruby constructs: %d probes, %d answers, %d traces, " \
            "%d raises, %d refusals, %.1f s",
            $done, $ans, $tr, $raises, $refused, el)
OUT.write("__SUMMARY__|#{$done}|#{$ans}|#{$tr}|#{$raises}|#{$refused}|" \
          "#{format('%.3f', el)}\n")
OUT.close
'''



PHP_DRIVER = r'''
<?php
$ROOT = $argv[1];
$T = json_decode(file_get_contents($ROOT . "/table.json"), true);
$HS = $T["holders"]; $CONS = $T["constructs"];
$AUG = $T["aug_ops"]; $KMAX = $T["jump_k"];
$START = intval($argv[2]);
$OUT = fopen("/out/kc_php.txt", $START == 0 ? "w" : "a");
$IDX = "/work/kc_php/idx";

function hms($x) {
  if ($x === null || $x < 0) return "--:--:--";
  $x = (int)$x;
  return sprintf("%02d:%02d:%02d", intdiv($x,3600), intdiv($x%3600,60), $x%60);
}

function enc($v, $d = 0) {
  if ($d > 3) return "OPAQUE:" . bin2hex(substr(print_r($v, true), 0, 40));
  if (is_null($v)) return "NULL";
  if ($v === true) return "BOOL:true";
  if ($v === false) return "BOOL:false";
  if (is_int($v)) return sprintf("INT:64:%016x", $v);
  if (is_float($v)) {
    $b = unpack("Q", pack("d", $v));
    return sprintf("FLOAT:64:%016x", $b[1]);
  }
  if (is_string($v)) {
    $n = function_exists("mb_strlen") ? @mb_strlen($v, "UTF-8") : strlen($v);
    if ($n === false) $n = strlen($v);
    return sprintf("STR:%d:%d:%s", $n, strlen($v),
                   bin2hex(substr($v, 0, 64)));
  }
  if (is_array($v)) {
    $keys = array_keys($v);
    $isList = $keys === range(0, count($v) - 1);
    $xs = [];
    foreach (array_slice($v, 0, 8, true) as $k => $w) {
      $xs[] = $isList ? enc($w, $d+1)
                      : enc($k, $d+1) . "=>" . enc($w, $d+1);
    }
    if (!$isList) sort($xs);
    return sprintf("%s:%d[%s]", $isList ? "LIST" : "MAP",
                   count($v), implode(",", $xs));
  }
  if (is_object($v)) {
    return "OPAQUE:" . bin2hex(substr(get_class($v), 0, 40));
  }
  return "OPAQUE:" . bin2hex(substr(print_r($v, true), 0, 40));
}

function tn($v) {
  if (is_object($v)) return get_class($v);
  return gettype($v);
}

$SCAF = [
 "access.subscript"  => "\$__r = (\$a)[(\$b)];\n",
 "access.member"     => "\$__r = (\$a)->f;\n",
 "flow.if"           => "if (\$a) { \$__t[] = 'BR=then'; } else { \$__t[] = 'BR=else'; }\n",
 "flow.for"          => "\$__n = 0;\nforeach ((\$a) as \$__v) {\n" .
                        "  \$__t[] = 'IT=' . enc(\$__v); \$__n++;\n" .
                        "  if (\$__n >= 8) { \$__t[] = \"STOP=\$__n\"; break; }\n}\n",
 "flow.while"        => "\$__n = 0;\nwhile (\$a) {\n" .
                        "  \$__t[] = 'IT=' . enc(\$__n); \$__n++;\n" .
                        "  if (\$__n >= 8) { \$__t[] = \"STOP=\$__n\"; break; }\n}\n",
 "flow.try"          => "try {\n  \$__t[] = 'BR=try';\n  \$__z = (\$a)[0];\n" .
                        "} catch (\\Throwable \$__e) {\n  \$__t[] = 'BR=catch';\n" .
                        "  \$__t[] = 'THROW=' . get_class(\$__e);\n" .
                        "} finally {\n  \$__t[] = 'BR=finally';\n}\n",
 "flow.break"        => "foreach ([1,2,3,4,5] as \$__v) {\n" .
                        "  if (\$__v == {K}) { \$__t[] = 'STOP=' . (\$__v - 1); break; }\n" .
                        "  \$__t[] = 'IT=' . enc(\$__v);\n}\n",
 "flow.continue"     => "foreach ([1,2,3,4,5] as \$__v) {\n" .
                        "  if (\$__v == {K}) { \$__t[] = 'SKIP=' . \$__v; continue; }\n" .
                        "  \$__t[] = 'IT=' . enc(\$__v);\n}\n",
 "binding.assign"    => "\$__x = (\$a);\n\$__t[] = 'BIND=' . enc(\$__x);\n",
 "binding.augassign" => "\$__x = (\$a);\n\$__x {OP} (\$b);\n\$__t[] = 'BIND=' . enc(\$__x);\n",
];
$TRACE_CONS = [];
foreach ($SCAF as $k => $_) {
  if (str_starts_with($k, "flow.") || str_starts_with($k, "binding.")) {
    $TRACE_CONS[$k] = true;
  }
}

function rn($s, $n) { return preg_replace('/\\$v\\b/', '\\$' . $n, $s); }

// php refuses a class declared twice in one process, and two holders
// carry `class R0 {}` in their declaration text.  Every eval would
// redeclare it and the FATAL is not catchable -- the same shape as the
// log_027 5.1 fault.  The declared name is therefore suffixed per
// probe, mechanically, over the literal text.  SURFACED, not buried:
// this is a harness decision, it touches php only, and deleting this
// function reverses it.
function uniqcls($src, $n) {
  if (!preg_match_all('/\bclass\s+([A-Za-z_]\w*)/', $src, $m)) return $src;
  foreach (array_unique($m[1]) as $name) {
    $src = preg_replace('/\b' . preg_quote($name, '/') . '\b/',
                        $name . '_' . $n, $src);
  }
  return $src;
}

$V = 0; foreach ($HS as $h) $V += count($h["values"]);
$M = 0;
foreach ($HS as $a) foreach ($HS as $b)
  $M += count($a["values"]) * count($b["values"]);
$total = 0;
foreach ($CONS as $c) {
  if (!isset($SCAF[$c])) continue;
  if ($c == "flow.break" || $c == "flow.continue") $total += $KMAX;
  elseif ($c == "access.subscript") $total += $M;
  elseif ($c == "binding.augassign") $total += $M * count($AUG);
  else $total += $V;
}
if ($START == 0) {
  fwrite(STDOUT, "CONSTRUCTS php: " . count($HS) . " holders, $V values, " .
         count($CONS) . " constructs, $total probes\n");
  flush();
}

$plan = [];
foreach ($CONS as $c) {
  if (!isset($SCAF[$c])) continue;
  $sc = $SCAF[$c];
  if ($c == "flow.break" || $c == "flow.continue") {
    for ($k = 1; $k <= $KMAX; $k++)
      $plan[] = ["K{$c}_{$k}", str_replace("{K}", (string)$k, $sc), "trace"];
    continue;
  }
  if ($c == "access.subscript") {
    foreach ($HS as $i => $ha) foreach ($HS as $j => $hb) {
      $va = $ha["values"]; ksort($va);
      $vb = $hb["values"]; ksort($vb);
      foreach ($va as $vca => $da) foreach ($vb as $vcb => $db)
        $plan[] = ["K{$c}_{$i}_{$j}_{$vca}_{$vcb}",
                   rn($da, "a") . "\n" . rn($db, "b") . "\n" . $sc, "answer"];
    }
    continue;
  }
  if ($c == "binding.augassign") {
    foreach ($HS as $i => $ha) foreach ($HS as $j => $hb) {
      $va = $ha["values"]; ksort($va);
      $vb = $hb["values"]; ksort($vb);
      foreach ($va as $vca => $da) foreach ($vb as $vcb => $db) {
        $head = rn($da, "a") . "\n" . rn($db, "b") . "\n";
        foreach ($AUG as $op)
          $plan[] = ["K{$c}{$op}_{$i}_{$j}_{$vca}_{$vcb}",
                     $head . str_replace("{OP}", $op, $sc), "trace"];
      }
    }
    continue;
  }
  $kind = isset($TRACE_CONS[$c]) ? "trace" : "answer";
  foreach ($HS as $i => $ha) {
    $va = $ha["values"]; ksort($va);
    foreach ($va as $vca => $da)
      $plan[] = ["K{$c}_{$i}_{$vca}", rn($da, "a") . "\n" . $sc, $kind];
  }
}

$t0 = microtime(true);
$ans = 0; $tr = 0; $raises = 0;
for ($n = $START; $n < count($plan); $n++) {
  list($pid, $src, $kind) = $plan[$n];
  file_put_contents($IDX, (string)($n + 1));
  $__t = [];
  $src = uniqcls($src, $n);
  try {
    $__r = null;
    eval($src);
    if ($kind == "answer") {
      fwrite($OUT, "$pid|" . tn($__r) . "|" . enc($__r) . "\n"); $ans++;
    } else {
      fwrite($OUT, "$pid|-|TRACE:" . count($__t) . "[" .
             implode(",", $__t) . "]\n"); $tr++;
    }
  } catch (\Throwable $e) {
    fwrite($OUT, "$pid|-|RAISE:" . get_class($e) . "\n"); $raises++;
  }
  if (($n + 1) % 5000 == 0) {
    $el = microtime(true) - $t0; $d = $n + 1 - $START;
    fwrite(STDOUT, sprintf("[progress] php constructs [%d/%d] %5.1f%%  " .
      "elapsed %s  ETA %s  mean %.2f ms", $n + 1, count($plan),
      100.0 * ($n + 1) / count($plan), hms($el),
      hms($el / $d * (count($plan) - $n - 1)), 1000.0 * $el / $d));
    fwrite(STDOUT, "\n"); flush();
  }
}
$el = microtime(true) - $t0;
fwrite(STDOUT, sprintf("== php constructs: %d probes, %d answers, %d traces, " .
  "%d raises, %.1f s\n", count($plan) - $START, $ans, $tr, $raises, $el));
fwrite($OUT, sprintf("__SUMMARY__|%d|%d|%d|%d|%.3f\n",
  count($plan) - $START, $ans, $tr, $raises, $el));
file_put_contents($IDX, (string)count($plan));
fclose($OUT);
'''


def b64gz(text):
    raw = gzip.compress(text.encode("utf-8"), 9)
    return base64.b64encode(raw).decode("ascii")


def wrap64(s, n=76):
    return "\n".join(s[i:i+n] for i in range(0, len(s), n))


def lane_python():
    lang = "python"
    tab = json.dumps(table(lang))
    drv = "import sys\nROOT = sys.argv[1]\n" + PY_DRIVER
    sh = []
    sh.append("#!/bin/sh")
    sh.append("# layer-3 CONSTRUCT lane -- python -- generated by "
              "l3_construct.py")
    sh.append("# Design: construct_design.md (2026-08-19), the owner's blessed")
    sh.append("# access / flow / binding families.  Route C: execution is")
    sh.append("# the only acceptance evidence python has.")
    sh.append("set -u")
    sh.append("export HOME=/work")
    sh.append("ROOT=/work/kc_python")
    sh.append('rm -rf "$ROOT"; mkdir -p "$ROOT"')
    sh.append('echo "=== layer-3 CONSTRUCTS -- python ==="')
    sh.append("date -u +%Y-%m-%dT%H:%M:%SZ")
    sh.append("df -Pm /work | awk 'NR==2{print \"free /work: \" $4 \" MB\"}'")
    sh.append("base64 -d <<'T_EOF' | gunzip > \"$ROOT/table.json\"")
    sh.append(wrap64(b64gz(tab)))
    sh.append("T_EOF")
    sh.append("base64 -d <<'D_EOF' > \"$ROOT/drv.py\"")
    sh.append(wrap64(base64.b64encode(drv.encode("utf-8")).decode("ascii")))
    sh.append("D_EOF")
    sh.append('python3 "$ROOT/drv.py" "$ROOT"')
    sh.append('echo "=== constructs python done ==="')
    sh.append("date -u +%Y-%m-%dT%H:%M:%SZ")
    p = os.path.join(LANES, "kc_python.sh")
    open(p, "w").write("\n".join(sh) + "\n")
    os.chmod(p, 0o755)
    return p




def lane_ruby():
    tab = json.dumps(table("ruby"))
    sh = ["#!/bin/sh",
          "# layer-3 CONSTRUCT lane -- ruby -- generated by l3_construct.py",
          "# Design: construct_design.md (2026-08-19).  Route C.",
          "set -u", "export HOME=/work", "ROOT=/work/kc_ruby",
          'rm -rf "$ROOT"; mkdir -p "$ROOT"',
          'echo "=== layer-3 CONSTRUCTS -- ruby ==="',
          "date -u +%Y-%m-%dT%H:%M:%SZ",
          "df -Pm /work | awk 'NR==2{print \"free /work: \" $4 \" MB\"}'",
          "base64 -d <<'T_EOF' | gunzip > \"$ROOT/table.json\"",
          wrap64(b64gz(tab)), "T_EOF",
          "base64 -d <<'D_EOF' > \"$ROOT/drv.rb\"",
          wrap64(base64.b64encode(RB_DRIVER.encode("utf-8")).decode("ascii")),
          "D_EOF",
          'ruby "$ROOT/drv.rb" "$ROOT"',
          'echo "=== constructs ruby done ==="',
          "date -u +%Y-%m-%dT%H:%M:%SZ"]
    p = os.path.join(LANES, "kc_ruby.sh")
    open(p, "w").write("\n".join(sh) + "\n")
    os.chmod(p, 0o755)
    return p


def lane_php():
    """php dies on a FATAL, which no catch reaches.  The driver takes a
    start index and writes the index it is on, so the shell restarts it
    past the corpse and a death costs exactly one probe -- the same
    posture answers_encoding.md gives DEATH."""
    tab = json.dumps(table("php"))
    sh = ["#!/bin/sh",
          "# layer-3 CONSTRUCT lane -- php -- generated by l3_construct.py",
          "# Design: construct_design.md (2026-08-19).  Route C.",
          "# A php FATAL is not catchable; the driver restarts past it.",
          "set -u", "export HOME=/work", "ROOT=/work/kc_php",
          'rm -rf "$ROOT"; mkdir -p "$ROOT"',
          'echo "=== layer-3 CONSTRUCTS -- php ==="',
          "date -u +%Y-%m-%dT%H:%M:%SZ",
          "df -Pm /work | awk 'NR==2{print \"free /work: \" $4 \" MB\"}'",
          "base64 -d <<'T_EOF' | gunzip > \"$ROOT/table.json\"",
          wrap64(b64gz(tab)), "T_EOF",
          "base64 -d <<'D_EOF' > \"$ROOT/drv.php\"",
          wrap64(base64.b64encode(PHP_DRIVER.encode("utf-8")).decode("ascii")),
          "D_EOF",
          'echo 0 > "$ROOT/idx"',
          "S=0",
          "R=0",
          "while [ $R -lt 400 ]; do",
          '  php -d memory_limit=1G "$ROOT/drv.php" "$ROOT" "$S" || true',
          '  N=$(cat "$ROOT/idx" 2>/dev/null || echo 0)',
          '  if [ "$N" -le "$S" ]; then N=$((S+1)); fi',
          '  LAST=$(tail -n 1 /out/kc_php.txt 2>/dev/null || echo "")',
          '  case "$LAST" in __SUMMARY__*) break;; esac',
          '  echo "[restart] php resuming at probe $N (fatal at $((N-1)))"',
          "  S=$N",
          "  R=$((R+1))",
          "done",
          'echo "=== constructs php done ==="',
          "date -u +%Y-%m-%dT%H:%M:%SZ"]
    p = os.path.join(LANES, "kc_php.sh")
    open(p, "w").write("\n".join(sh) + "\n")
    os.chmod(p, 0o755)
    return p


def main():
    print("layer-3 CONSTRUCT generation -- design: construct_design.md")
    for lang in ["python", "ruby", "php"]:
        m = manifest(lang)
        print("  %-11s manifest frozen: %d constructs present, "
              "%d acceptance + %d answer probes"
              % (lang,
                 sum(1 for c in m["constructs"].values() if c["present"]),
                 m["totals"]["acceptance"], m["totals"]["answers"]))
    for f in (lane_python, lane_ruby, lane_php):
        p = f()
        print("  wrote %s (%d bytes)" % (p, os.path.getsize(p)))


if __name__ == "__main__":
    main()
