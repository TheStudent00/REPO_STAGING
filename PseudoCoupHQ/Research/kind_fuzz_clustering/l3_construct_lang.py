#!/usr/bin/env python3
"""l3_construct_lang.py -- the CONSTRUCT lanes for the eight statically
checked languages that log 036 left unrun.

l3_construct_go.py is the worked example and HARVEST_constructs.md says
only two of its four parts change per language: the PRELUDE (the value
encoder and the trace recorder, written in that language) and the SCAF
table (the scaffold per construct, in that language's syntax).  This
file carries those two parts for eight languages and reuses everything
else.

The value encoders are NOT rewritten here.  They are lifted verbatim
from `l3_exec.py`'s RT_<lang>, which the operator pass already ran over
the whole value matrix in logs 032 and 033.  Reusing a measured encoder
is decision 15 ("constructs reuse the operator lane machinery") applied
to the one part of the lane that would otherwise be new code on the
evidence path.  What this file adds to each encoder is three lines of
trace recorder -- a buffer, an append, a dump -- which decision 5 calls
harness machinery.

Two stages per lane, in one dropped script.

  ACCEPTANCE   the language's own proven instrument, per CORE ruling 5
               and construct_design.md section g:
                 rust    rustc --emit=metadata, per file
                 cpp     g++ -std=c++20 -fsyntax-only, per file
                 swift   the FULL swiftc, never -typecheck (log 034)
                 dart    dart analyze --format=machine, ERROR only
                 csharp  Roslyn GetDiagnostics, in process
                 java    javax.tools JavacTask.analyze, in process
                 kotlin  K2JVMCompiler in a warm JVM, in process
                 ts      the shipped typescript.js Program diagnostics
  EXECUTION    the ACCEPTED probes only, assembled into chunks, one
               compile per chunk, the binary taking a START INDEX so an
               uncatchable death costs exactly one probe (log 032).

Both stages read the same scaffold text, which is what decision 4
demands.
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
from l3_accept import holders, base_value, rename         # noqa: E402
from l3_exec import RT                                    # noqa: E402
from l3_lanes import (DRV_CS, KDRV_JAVA, JDRV_JAVA,       # noqa: E402
                      TDRV_JS)
from construct_space import space, AUG_OPS, JUMP_K        # noqa: E402

LANGS = ["typescript", "csharp", "rust", "cpp", "dart", "java",
         "swift", "kotlin"]

EXT = dict(typescript="ts", csharp="cs", rust="rs", cpp="cpp",
           dart="dart", java="java", swift="swift", kotlin="kt")

# how many probes share one compile in the EXECUTION stage.
CHUNK = dict(typescript=400, csharp=300, rust=200, cpp=200, dart=300,
             java=300, swift=150, kotlin=300)

# ----------------------------------------------------------------------
# part 1 -- the trace recorder, per language.  Three lines each: a
# buffer, an append, a dump.  Harness machinery, decision 5.  The value
# encoder it leans on is RT_<lang> from l3_exec.py, unchanged.
# ----------------------------------------------------------------------
TRACE = {
 "typescript":
   # `process` is node's, not typescript's, and the acceptance route is
   # a ts Program with `types: []` -- no node type declarations loaded.
   # Without this line the RECORDER is what the checker refuses and
   # every probe scores REFUSE, which is the harness refusing rather
   # than the language.  Measured on the smoke run, 2026-08-19: 64 of
   # 64 REFUSE before the line, and it is erased by transpilation, so
   # the execution stage is untouched.
   'declare var process: any;\n'
   'const _t: string[] = [];\n'
   'function _T(s: string): void { _t.push(s); }\n'
   'function _dump(id: string): void {\n'
   '  process.stdout.write(\n'
   '    id + "|-|TRACE:" + _t.length + "[" + _t.join(",") + "]\\n");\n'
   '  _t.length = 0;\n}\n',
 "csharp":
   'static class TR {\n'
   '  public static System.Collections.Generic.List<string> B =\n'
   '    new System.Collections.Generic.List<string>();\n'
   '  public static void T(string s) { B.Add(s); }\n'
   '  public static void Dump(string id) {\n'
   '    System.Console.Out.Write(id + "|-|TRACE:" +\n'
   '      B.Count + "[" + string.Join(",", B) + "]\\n");\n'
   '    B.Clear(); System.Console.Out.Flush();\n  }\n}\n',
 "rust":
   'thread_local!(static _TB: std::cell::RefCell<Vec<String>> =\n'
   '    std::cell::RefCell::new(Vec::new()));\n'
   'fn _T(s: String) { _TB.with(|b| b.borrow_mut().push(s)); }\n'
   'fn _dump(id: &str) {\n'
   '    _TB.with(|b| {\n'
   '        let mut v = b.borrow_mut();\n'
   '        println!("{}|-|TRACE:{}[{}]", id, v.len(), v.join(","));\n'
   '        v.clear();\n    });\n}\n',
 "cpp":
   '#include <vector>\n#include <string>\n'
   'static std::vector<std::string> _TB;\n'
   'static void _T(const std::string &s) { _TB.push_back(s); }\n'
   'static void _dump(const char *id) {\n'
   '  {\n'
   '    std::string s;\n'
   '    for (size_t i = 0; i < _TB.size(); i++) {\n'
   '      if (i) s += ","; s += _TB[i];\n    }\n'
   '    printf("%s|-|TRACE:%d[%s]\\n", id, (int)_TB.size(), s.c_str());\n'
   '    fflush(stdout);\n  }\n  _TB.clear();\n}\n',
 "dart":
   'final List<String> _TB = <String>[];\n'
   'void _T(String s) { _TB.add(s); }\n'
   'void _dump(String id) {\n'
   "  stdout.writeln(id + '|-|TRACE:' +\n"
   "      _TB.length.toString() + '[' + _TB.join(',') + ']');\n"
   '  _TB.clear();\n}\n',
 "java":
   'class TR {\n'
   '  static java.util.List<String> B = new java.util.ArrayList<String>();\n'
   '  static void T(String s) { B.add(s); }\n'
   '  static void dump(String id) {\n'
   '    System.out.println(id + "|-|TRACE:" + B.size()\n'
   '      + "[" + String.join(",", B) + "]");\n'
   '    B.clear(); System.out.flush();\n  }\n}\n',
 "swift":
   'var _TB: [String] = []\n'
   'func _T(_ s: String) { _TB.append(s) }\n'
   'func _dump(_ id: String) {\n'
   '  print(id + "|-|TRACE:" + String(_TB.count) + "["\n'
   '        + _TB.joined(separator: ",") + "]")\n  _TB = []\n}\n',
 "kotlin":
   'object TR {\n'
   '  val B = ArrayList<String>()\n'
   '  fun T(s: String) { B.add(s) }\n'
   '  fun dump(id: String) {\n'
   '    println(id + "|-|TRACE:" + B.size + "[" +\n'
   '        B.joinToString(",") + "]")\n'
   '    B.clear(); System.out.flush()\n  }\n}\n',
}

# ----------------------------------------------------------------------
# part 2 -- the SCAF table, per language.  Fixed, minimal, inert
# (decision 4).  {A} is always the local `a`, {B} `b`, {C} `c`; {K} is
# the jump position and {OP} the augmented operation.  ~ID~ is replaced
# with the probe id when the probe is written out.
# ----------------------------------------------------------------------
SCAF = {
 "typescript": {
  "access.subscript": 'let _r = (a)[(b)];\n_emit("~ID~", _r);\n',
  "access.member":    'let _r = (a).f;\n_emit("~ID~", _r);\n',
  "flow.if":          'if ((a)) { _T("BR=then"); } else { _T("BR=else"); }\n',
  "flow.for":         'let _n = 0;\nfor (const _v of (a)) {\n'
                      '  _T("IT=" + _enc(_v)); _n++;\n'
                      '  if (_n >= 8) { _T("STOP=" + _n); break; }\n}\n',
  "flow.while":       'let _n = 0;\nwhile ((a)) {\n'
                      '  _T("IT=" + _enc(_n)); _n++;\n'
                      '  if (_n >= 8) { _T("STOP=" + _n); break; }\n}\n',
  "flow.try":         'try { _T("BR=try"); let _z = (a)[0]; }\n'
                      'catch (_e: any) { _T("BR=catch");\n'
                      '  _T("THROW=" + ((_e && _e.constructor &&\n'
                      '    _e.constructor.name) || "error")); }\n'
                      'finally { _T("BR=finally"); }\n',
  "flow.break":       'for (const _v of [1, 2, 3, 4, 5]) {\n'
                      '  if (_v === {K}) { _T("STOP=" + (_v - 1)); break; }\n'
                      '  _T("IT=" + _enc(_v));\n}\n',
  "flow.continue":    'for (const _v of [1, 2, 3, 4, 5]) {\n'
                      '  if (_v === {K}) { _T("SKIP=" + _v); continue; }\n'
                      '  _T("IT=" + _enc(_v));\n}\n',
  "binding.assign":   'let _x = (a);\n_T("BIND=" + _enc(_x));\n',
  "binding.augassign": 'let _x = (a);\n_x {OP} (b);\n'
                       '_T("BIND=" + _enc(_x));\n',
  "binding.unpack":   'const [_p, _q] = (a);\n_T("BIND=" + _enc(_p));\n'
                      '_T("BIND=" + _enc(_q));\n',
 },
 "csharp": {
  "access.subscript": 'var _r = (a)[(b)];\nRT.Emit("~ID~", _r);\n',
  "access.slice":     'var _r = (a)[(b)..(c)];\nRT.Emit("~ID~", _r);\n',
  "access.member":    'var _r = (a).f;\nRT.Emit("~ID~", _r);\n',
  "flow.if":          'if ((a)) { TR.T("BR=then"); } else { TR.T("BR=else"); }\n',
  "flow.for":         'var _n = 0;\nforeach (var _v in (a)) {\n'
                      '  TR.T("IT=" + RT.Enc(_v)); _n++;\n'
                      '  if (_n >= 8) { TR.T("STOP=" + _n); break; }\n}\n',
  "flow.while":       'var _n = 0;\nwhile ((a)) {\n'
                      '  TR.T("IT=" + RT.Enc(_n)); _n++;\n'
                      '  if (_n >= 8) { TR.T("STOP=" + _n); break; }\n}\n',
  "flow.try":         'try { TR.T("BR=try"); var _z = (a)[0]; }\n'
                      'catch (System.Exception _e) { TR.T("BR=catch");\n'
                      '  TR.T("THROW=" + _e.GetType().FullName); }\n'
                      'finally { TR.T("BR=finally"); }\n',
  "flow.break":       'foreach (var _v in new int[] {1, 2, 3, 4, 5}) {\n'
                      '  if (_v == {K}) { TR.T("STOP=" + (_v - 1)); break; }\n'
                      '  TR.T("IT=" + RT.Enc(_v));\n}\n',
  "flow.continue":    'foreach (var _v in new int[] {1, 2, 3, 4, 5}) {\n'
                      '  if (_v == {K}) { TR.T("SKIP=" + _v); continue; }\n'
                      '  TR.T("IT=" + RT.Enc(_v));\n}\n',
  "binding.assign":   'var _x = (a);\nTR.T("BIND=" + RT.Enc(_x));\n',
  "binding.augassign": 'var _x = (a);\n_x {OP} (b);\n'
                       'TR.T("BIND=" + RT.Enc(_x));\n',
  "binding.unpack":   'var (_p, _q) = (a);\nTR.T("BIND=" + RT.Enc(_p));\n'
                      'TR.T("BIND=" + RT.Enc(_q));\n',
 },
 "rust": {
  "access.subscript": 'let _r = &(a)[(b)];\n_emit("~ID~", _r);\n',
  "access.slice":     'let _r = &(a)[(b)..(c)];\n_emit("~ID~", _r);\n',
  "access.member":    'let _r = &(a).f;\n_emit("~ID~", _r);\n',
  "flow.if":          'if (a) { _T("BR=then".to_string()); }\n'
                      'else { _T("BR=else".to_string()); }\n',
  "flow.for":         'let mut _n = 0;\nfor _v in (a) {\n'
                      '    _T(format!("IT={}", (&_v).db())); _n += 1;\n'
                      '    if _n >= 8 { _T(format!("STOP={}", _n)); break; }\n}\n',
  "flow.while":       'let mut _n: i64 = 0;\nwhile (a) {\n'
                      '    _T(format!("IT={}", (&_n).db())); _n += 1;\n'
                      '    if _n >= 8 { _T(format!("STOP={}", _n)); break; }\n}\n',
  "flow.try":         'let _q = (|| {\n'
                      '    _T("BR=try".to_string());\n'
                      '    let _z = (a)?;\n    Some(_z)\n})();\n'
                      'if _q.is_none() { _T("BR=catch".to_string()); }\n',
  "flow.break":       'for _v in 1..=5 {\n'
                      '    if _v == {K} { _T(format!("STOP={}", _v - 1)); break; }\n'
                      '    _T(format!("IT={}", (&_v).db()));\n}\n',
  "flow.continue":    'for _v in 1..=5 {\n'
                      '    if _v == {K} { _T(format!("SKIP={}", _v)); continue; }\n'
                      '    _T(format!("IT={}", (&_v).db()));\n}\n',
  "binding.assign":   'let _x = (a);\n_T(format!("BIND={}", (&_x).db()));\n',
  "binding.augassign": 'let mut _x = (a);\n_x {OP} (b);\n'
                       '_T(format!("BIND={}", (&_x).db()));\n',
  "binding.unpack":   'let (_p, _q) = (a);\n'
                      '_T(format!("BIND={}", (&_p).db()));\n'
                      '_T(format!("BIND={}", (&_q).db()));\n',
 },
 "cpp": {
  "access.subscript": 'auto _r = (a)[(b)];\n_emit("~ID~", _r);\n',
  "access.member":    'auto _r = (a).f;\n_emit("~ID~", _r);\n',
  "flow.if":          'if ((a)) { _T("BR=then"); } else { _T("BR=else"); }\n',
  "flow.for":         'int _n = 0;\nfor (auto &&_v : (a)) {\n'
                      '  _T("IT=" + _enc(_v)); _n++;\n'
                      '  if (_n >= 8) { _T("STOP=" + std::to_string(_n)); break; }\n}\n',
  "flow.while":       'long long _n = 0;\nwhile ((a)) {\n'
                      '  _T("IT=" + _enc(_n)); _n++;\n'
                      '  if (_n >= 8) { _T("STOP=" + std::to_string(_n)); break; }\n}\n',
  "flow.try":         'try { _T("BR=try"); auto _z = (a)[0]; (void)_z; }\n'
                      'catch (const std::exception &_e) { _T("BR=catch");\n'
                      '  _T(std::string("THROW=") + _e.what()); }\n'
                      'catch (...) { _T("BR=catch"); _T("THROW=cxx"); }\n',
  "flow.break":       'for (int _v : {1, 2, 3, 4, 5}) {\n'
                      '  if (_v == {K}) { _T("STOP=" + std::to_string(_v - 1)); break; }\n'
                      '  _T("IT=" + _enc(_v));\n}\n',
  "flow.continue":    'for (int _v : {1, 2, 3, 4, 5}) {\n'
                      '  if (_v == {K}) { _T("SKIP=" + std::to_string(_v)); continue; }\n'
                      '  _T("IT=" + _enc(_v));\n}\n',
  "binding.assign":   'auto _x = (a);\n_T("BIND=" + _enc(_x));\n',
  "binding.augassign": 'auto _x = (a);\n_x {OP} (b);\n'
                       '_T("BIND=" + _enc(_x));\n',
  "binding.unpack":   'auto [_p, _q] = (a);\n_T("BIND=" + _enc(_p));\n'
                      '_T("BIND=" + _enc(_q));\n',
 },
 "dart": {
  "access.subscript": "var _r = (a)[(b)];\n_emit('~ID~', _r);\n",
  "access.member":    "var _r = (a).f;\n_emit('~ID~', _r);\n",
  "flow.if":          "if ((a)) { _T('BR=then'); } else { _T('BR=else'); }\n",
  "flow.for":         "var _n = 0;\nfor (var _v in (a)) {\n"
                      "  _T('IT=' + _enc(_v)); _n++;\n"
                      "  if (_n >= 8) { _T('STOP=' + _n.toString()); break; }\n}\n",
  "flow.while":       "var _n = 0;\nwhile ((a)) {\n"
                      "  _T('IT=' + _enc(_n)); _n++;\n"
                      "  if (_n >= 8) { _T('STOP=' + _n.toString()); break; }\n}\n",
  "flow.try":         "try { _T('BR=try'); var _z = (a)[0]; }\n"
                      "catch (_e) { _T('BR=catch');\n"
                      "  _T('THROW=' + _e.runtimeType.toString()); }\n"
                      "finally { _T('BR=finally'); }\n",
  "flow.break":       "for (var _v in [1, 2, 3, 4, 5]) {\n"
                      "  if (_v == {K}) { _T('STOP=' + (_v - 1).toString()); break; }\n"
                      "  _T('IT=' + _enc(_v));\n}\n",
  "flow.continue":    "for (var _v in [1, 2, 3, 4, 5]) {\n"
                      "  if (_v == {K}) { _T('SKIP=' + _v.toString()); continue; }\n"
                      "  _T('IT=' + _enc(_v));\n}\n",
  "binding.assign":   "var _x = (a);\n_T('BIND=' + _enc(_x));\n",
  "binding.augassign": "var _x = (a);\n_x {OP} (b);\n"
                       "_T('BIND=' + _enc(_x));\n",
  "binding.unpack":   "var (_p, _q) = (a);\n_T('BIND=' + _enc(_p));\n"
                      "_T('BIND=' + _enc(_q));\n",
 },
 "java": {
  "access.subscript": 'var _r = (a)[(b)];\nRT.emit("~ID~", _r);\n',
  "access.member":    'var _r = (a).f;\nRT.emit("~ID~", _r);\n',
  "flow.if":          'if ((a)) { TR.T("BR=then"); } else { TR.T("BR=else"); }\n',
  "flow.for":         'var _n = 0;\nfor (var _v : (a)) {\n'
                      '  TR.T("IT=" + RT.enc(_v)); _n++;\n'
                      '  if (_n >= 8) { TR.T("STOP=" + _n); break; }\n}\n',
  "flow.while":       'var _n = 0;\nwhile ((a)) {\n'
                      '  TR.T("IT=" + RT.enc(_n)); _n++;\n'
                      '  if (_n >= 8) { TR.T("STOP=" + _n); break; }\n}\n',
  "flow.try":         'try { TR.T("BR=try"); var _z = (a)[0]; }\n'
                      'catch (Throwable _e) { TR.T("BR=catch");\n'
                      '  TR.T("THROW=" + _e.getClass().getName()); }\n'
                      'finally { TR.T("BR=finally"); }\n',
  "flow.break":       'for (int _v : new int[] {1, 2, 3, 4, 5}) {\n'
                      '  if (_v == {K}) { TR.T("STOP=" + (_v - 1)); break; }\n'
                      '  TR.T("IT=" + RT.enc(_v));\n}\n',
  "flow.continue":    'for (int _v : new int[] {1, 2, 3, 4, 5}) {\n'
                      '  if (_v == {K}) { TR.T("SKIP=" + _v); continue; }\n'
                      '  TR.T("IT=" + RT.enc(_v));\n}\n',
  "binding.assign":   'var _x = (a);\nTR.T("BIND=" + RT.enc(_x));\n',
  "binding.augassign": 'var _x = (a);\n_x {OP} (b);\n'
                       'TR.T("BIND=" + RT.enc(_x));\n',
 },
 "swift": {
  "access.subscript": 'let _r = (a)[(b)]\n_emit("~ID~", _r)\n',
  "flow.if":          'if (a) { _T("BR=then") } else { _T("BR=else") }\n',
  "flow.for":         'var _n = 0\nfor _v in (a) {\n'
                      '  _T("IT=" + _enc(_v))\n  _n += 1\n'
                      '  if _n >= 8 { _T("STOP=" + String(_n)); break }\n}\n',
  "flow.while":       'var _n = 0\nwhile (a) {\n'
                      '  _T("IT=" + _enc(_n))\n  _n += 1\n'
                      '  if _n >= 8 { _T("STOP=" + String(_n)); break }\n}\n',
  "flow.break":       'for _v in [1, 2, 3, 4, 5] {\n'
                      '  if _v == {K} { _T("STOP=" + String(_v - 1)); break }\n'
                      '  _T("IT=" + _enc(_v))\n}\n',
  "flow.continue":    'for _v in [1, 2, 3, 4, 5] {\n'
                      '  if _v == {K} { _T("SKIP=" + String(_v)); continue }\n'
                      '  _T("IT=" + _enc(_v))\n}\n',
  "binding.assign":   'let _x = (a)\n_T("BIND=" + _enc(_x))\n',
  "binding.unpack":   'let (_p, _q) = (a)\n_T("BIND=" + _enc(_p))\n'
                      '_T("BIND=" + _enc(_q))\n',
 },
 "kotlin": {
  "access.subscript": 'val _r = (a)[(b)]\nRT.emit("~ID~", _r)\n',
  "access.slice":     'val _r = (a)[(b)..(c)]\nRT.emit("~ID~", _r)\n',
  "access.member":    'val _r = (a).f\nRT.emit("~ID~", _r)\n',
  "flow.if":          'if ((a)) { TR.T("BR=then") } else { TR.T("BR=else") }\n',
  "flow.for":         'var _n = 0\nfor (_v in (a)) {\n'
                      '  TR.T("IT=" + RT.enc(_v)); _n++\n'
                      '  if (_n >= 8) { TR.T("STOP=" + _n); break }\n}\n',
  "flow.while":       'var _n = 0\nwhile ((a)) {\n'
                      '  TR.T("IT=" + RT.enc(_n)); _n++\n'
                      '  if (_n >= 8) { TR.T("STOP=" + _n); break }\n}\n',
  "flow.try":         'try { TR.T("BR=try"); val _z = (a)[0] }\n'
                      'catch (_e: Throwable) { TR.T("BR=catch")\n'
                      '  TR.T("THROW=" + _e.javaClass.name) }\n'
                      'finally { TR.T("BR=finally") }\n',
  "binding.assign":   'val _x = (a)\nTR.T("BIND=" + RT.enc(_x))\n',
  "binding.augassign": 'var _x = (a)\n_x {OP} (b)\n'
                       'TR.T("BIND=" + RT.enc(_x))\n',
  "binding.unpack":   'val (_p, _q) = (a)\nTR.T("BIND=" + RT.enc(_p))\n'
                      'TR.T("BIND=" + RT.enc(_q))\n',
 },
}

# a role the GRAMMAR declares but the LANGUAGE cannot honestly probe.
# The go lane opened this door for binding.unpack (design decision 16);
# these are the same shape and each carries its reason.
NOT_APPLICABLE = {
 "java": {"binding.unpack":
          "java's record_pattern destructures inside `instanceof` and "
          "`switch`, never a binding statement; there is no java "
          "`var (p, q) = a`"},
 "swift": {},
 "typescript": {}, "csharp": {}, "rust": {}, "cpp": {},
 "dart": {}, "kotlin": {},
}

ANSWER_CONS = {"access.subscript", "access.slice", "access.member"}


# ----------------------------------------------------------------------
# part 3 -- gen_acceptance.  UNCHANGED from l3_construct_go.py except
# that the scaffold table is looked up per language.
# ----------------------------------------------------------------------
def pres_for(lang, holder_list, used_text):
    """the holder `pre` lines this probe needs, deduplicated.

    An unused import is a refusal in go and rust, so a pre line whose
    last identifier never appears in the probe text is dropped.  This
    cost the go lane two runs (HARVEST_constructs.md)."""
    lines = []
    for h in holder_list:
        for line in (h.get("pre") or "").splitlines():
            line = line.strip()
            if not line:
                continue
            if lang in ("go", "rust"):
                m = re.findall(r"[A-Za-z_][A-Za-z_0-9]*", line)
                tok = m[-1] if m else ""
                if tok and tok not in used_text:
                    continue
            if line not in lines:
                lines.append(line)
    return lines


def gen_probes(lang):
    """[(pid, construct, pres, decls, body)] -- the acceptance grain."""
    hs, _ = holders(lang)
    sp = space(lang)
    present = [r["construct"] for r in sp["constructs"] if r["present"]]
    na = NOT_APPLICABLE.get(lang, {})
    out = []
    wi = next((n for n, h in enumerate(hs) if h["form"] == "whole"), None)
    for cons in present:
        if cons in na:
            continue
        if cons not in SCAF[lang]:
            continue
        sc = SCAF[lang][cons]
        if cons in ("flow.break", "flow.continue"):
            for k in range(1, JUMP_K + 1):
                pid = "K%s_%d" % (cons, k)
                out.append((pid, cons, [], [],
                            sc.replace("{K}", str(k))))
            continue
        two = cons in ("access.subscript", "binding.augassign")
        three = cons == "access.slice"
        for i, ha in enumerate(hs):
            da = rename(base_value(ha)[1], "a")
            if three:
                if wi is None:
                    continue
                db = rename(base_value(hs[wi])[1], "b")
                dc = rename(base_value(hs[wi])[1], "c")
                pid = "K%s_%d" % (cons, i)
                out.append((pid, cons,
                            pres_for(lang, [ha, hs[wi]], da + db + dc + sc),
                            [da, db, dc], sc))
                continue
            if not two:
                pid = "K%s_%d" % (cons, i)
                out.append((pid, cons, pres_for(lang, [ha], da + sc),
                            [da], sc))
                continue
            for j, hb in enumerate(hs):
                db = rename(base_value(hb)[1], "b")
                ops = AUG_OPS if cons == "binding.augassign" else [""]
                for op in ops:
                    body = sc.replace("{OP}", op)
                    pid = "K%s%s_%d_%d" % (cons, op, i, j)
                    out.append((pid, cons,
                                pres_for(lang, [ha, hb], da + db + body),
                                [da, db], body))
    return out


# ----------------------------------------------------------------------
# part 4 -- source assembly.  ONE probe per file for the acceptance
# stage; MANY probes per file for the execution stage.  Both read the
# same scaffold text.
# ----------------------------------------------------------------------
SRCGEN = r'''
def _dedup(seq):
    o = []
    for s in seq:
        if s not in o:
            o.append(s)
    return o


def _split(lines, kw):
    h, b = [], []
    for l in lines:
        (h if l.startswith(kw) else b).append(l)
    return h, b


def one(lang, rt, tr, p):
    """the acceptance file: one probe, alone, in its own program."""
    return chunk(lang, rt, tr, [p], solo=True)


def chunk(lang, rt, tr, ps, solo=False):
    """one program carrying len(ps) probes; the binary takes a start
    index so a death costs one probe (log 032)."""
    pres = _dedup([l for p in ps for l in p[2]])
    n = len(ps)

    def marked(fmt, cmt="//"):
        return "".join("%s __PROBE__ %s\n%s" % (cmt, p[0], fmt(i, p))
                       for i, p in enumerate(ps)) + "%s __PROBE__ -\n" % cmt

    def body(p):
        return "\n".join(p[3]) + "\n" + p[4].replace("~ID~", p[0])

    def dmp(p, call):
        # exactly one row per probe.  An ANSWER construct's row comes
        # from _emit; a FLOW or BINDING construct's row comes from the
        # trace dump, and the dump fires even when the trace is empty,
        # because "the construct ran and recorded nothing" is a
        # measurement and a missing row is not.
        return call if p[1].startswith(("flow.", "binding.")) else ""

    def ind(t, k):
        return "\n".join((" " * k + l if l.strip() else l)
                         for l in t.splitlines()) + "\n"

    if lang == "typescript":
        src = "\n".join(pres) + "\n" + rt + "\n" + tr + "\n"
        src += marked(lambda i, p:
            'function pr%d(): void {\n  try {\n%s  } catch (_e: any) {\n'
            '    process.stdout.write("%s|-|RAISE:" + ((_e && _e.constructor'
            ' && _e.constructor.name) || "error") + "\\n");\n    return;\n'
            '  }\n%s}\n'
            % (i, ind(body(p), 4), p[0], dmp(p, '  _dump("%s");\n' % p[0])))
        src += "const _P: Array<() => void> = [\n"
        src += "".join("  pr%d,\n" % i for i in range(n))
        src += ("];\nconst _s: number = process.argv.length > 2 ?"
                " parseInt(process.argv[2]) : 0;\n"
                "for (let i = _s; i < _P.length; i++) { _P[i](); }\n"
                'process.stdout.write("__END__\\n");\nexport {};\n')
        return src, "chunk.ts"

    if lang == "csharp":
        rh, rb = _split(rt.splitlines(), "using ")
        ph, pb = _split(pres, "using ")
        src = "\n".join(_dedup(ph + rh)) + "\n" + "\n".join(pb) + "\n"
        src += "\n".join(rb) + "\n" + tr + "\nclass Chunk {\n"
        src += marked(lambda i, p:
            '  static void pr%d() {\n    try {\n%s    } catch '
            '(System.Exception _e) {\n      RT.Raise("%s",'
            ' _e.GetType().FullName);\n      return;\n    }\n%s  }\n'
            % (i, ind(body(p), 6), p[0],
               dmp(p, '    TR.Dump("%s");\n' % p[0])))
        for g in range(0, n, 100):
            src += "  static void d%d(int i) {\n    switch (i) {\n" % (g // 100)
            for i in range(g, min(g + 100, n)):
                src += "      case %d: pr%d(); break;\n" % (i, i)
            src += "    }\n  }\n"
        src += "  static void Run(int i) {\n    switch (i / 100) {\n"
        for g in range(0, n, 100):
            src += "      case %d: d%d(i); break;\n" % (g // 100, g // 100)
        src += "    }\n  }\n"
        src += ('  static void Main(string[] a) {\n    int s = a.Length > 0'
                ' ? int.Parse(a[0]) : 0;\n'
                '    for (int i = s; i < %d; i++) Run(i);\n'
                '    System.Console.Out.Write("__END__\\n");\n'
                '    System.Console.Out.Flush();\n  }\n}\n' % n)
        return src, "Chunk.cs"

    if lang == "rust":
        src = ("#![allow(unused, non_snake_case, non_camel_case_types,"
               " unused_parens, unused_mut, unused_variables, dead_code,"
               " unconditional_panic, arithmetic_overflow)]\n")
        src += "\n".join(pres) + "\n" + rt + "\n" + tr + "\n"
        src += marked(lambda i, p:
            'fn pr%d() {\n%s%s}\n'
            % (i, ind(body(p), 4),
               dmp(p, '    _dump("%s");\n' % p[0])))
        src += "fn main() {\n    std::panic::set_hook(Box::new(|_| {}));\n"
        src += "    let ps: Vec<(&str, fn())> = vec![\n"
        src += "".join('        ("%s", pr%d),\n' % (p[0], i)
                       for i, p in enumerate(ps))
        src += "    ];\n    let av: Vec<String> = std::env::args().collect();\n"
        src += ("    let s: usize = if av.len() > 1 "
                "{ av[1].parse().unwrap_or(0) } else { 0 };\n")
        src += ("    for i in s..ps.len() {\n        let (id, f) = ps[i];\n"
                "        if std::panic::catch_unwind(f).is_err()\n"
                '            { println!("{}|-|RAISE:panic", id); }\n    }\n')
        src += '    println!("__END__");\n}\n'
        return src, "chunk.rs"

    if lang == "cpp":
        src = rt + "\n" + tr + "\n" + "\n".join(pres) + "\n"
        src += marked(lambda i, p:
            'static void pr%d() {\n  try {\n%s  } catch (const std::exception'
            ' &_e) {\n    _raise("%s", _e.what());\n    return;\n'
            '  } catch (...) {\n'
            '    _raise("%s", "cxx");\n    return;\n  }\n%s}\n'
            % (i, ind(body(p), 4), p[0], p[0],
               dmp(p, '  _dump("%s");\n' % p[0])))
        src += "typedef void (*_FN)();\nstatic _FN _P[] = {\n"
        src += "".join("  pr%d,\n" % i for i in range(n))
        src += "};\n\nint main(int argc, char** argv) {\n"
        src += "  size_t nn = %d;\n" % n
        src += "  size_t s = argc > 1 ? (size_t)atol(argv[1]) : 0;\n"
        src += "  for (size_t i = s; i < nn; i++) { _P[i](); }\n"
        src += '  printf("__END__\\n");\n  return 0;\n}\n'
        return src, "chunk.cpp"

    if lang == "dart":
        ph, pb = _split(pres, "import ")
        src = "\n".join(ph) + "\n" + rt + "\n" + tr + "\n" + "\n".join(pb) + "\n"
        src += marked(lambda i, p:
            "void pr%d() {\n  try {\n%s  } catch (_e) {\n"
            "    stdout.writeln('%s|-|RAISE:' + _e.runtimeType.toString());\n"
            "    return;\n  }\n%s}\n"
            % (i, ind(body(p), 4), p[0],
               dmp(p, "  _dump('%s');\n" % p[0])))
        src += "final _P = <void Function()>[\n"
        src += "".join("  pr%d,\n" % i for i in range(n))
        src += "];\n\nvoid main(List<String> args) {\n"
        src += "  var s = args.isNotEmpty ? int.parse(args[0]) : 0;\n"
        src += "  for (var i = s; i < _P.length; i++) { _P[i](); }\n"
        src += "  stdout.writeln('__END__');\n}\n"
        return src, "chunk.dart"

    if lang == "java":
        rh, rb = _split(rt.splitlines(), "import ")
        ph, pb = _split(pres, "import ")
        src = "\n".join(_dedup(ph + rh)) + "\n" + "\n".join(pb) + "\n"
        src += "\n".join(rb) + "\n" + tr + "\nclass Chunk {\n"
        src += marked(lambda i, p:
            '  static void pr%d() {\n    try {\n%s    } catch (Throwable _e)'
            ' {\n      RT.raise("%s", _e);\n      return;\n    }\n%s  }\n'
            % (i, ind(body(p), 6), p[0],
               dmp(p, '    TR.dump("%s");\n' % p[0])))
        for g in range(0, n, 100):
            src += "  static void d%d(int i) {\n    switch (i) {\n" % (g // 100)
            for i in range(g, min(g + 100, n)):
                src += "      case %d: pr%d(); break;\n" % (i, i)
            src += "    }\n  }\n"
        src += "  static void run(int i) {\n    switch (i / 100) {\n"
        for g in range(0, n, 100):
            src += "      case %d: d%d(i); break;\n" % (g // 100, g // 100)
        src += "    }\n  }\n"
        src += ('  public static void main(String[] a) {\n    int s ='
                ' a.length > 0 ? Integer.parseInt(a[0]) : 0;\n'
                '    for (int i = s; i < %d; i++) run(i);\n'
                '    System.out.println("__END__");\n  }\n}\n' % n)
        return src, "Chunk.java"

    if lang == "kotlin":
        rh, rb = _split(rt.splitlines(), "import ")
        ph, pb = _split(pres, "import ")
        src = "\n".join(_dedup(ph + rh)) + "\n" + "\n".join(pb) + "\n"
        src += "\n".join(rb) + "\n" + tr + "\n"
        src += marked(lambda i, p:
            'fun pr%d() {\n  try {\n%s  } catch (_e: Throwable) {\n'
            '    RT.raise("%s", _e)\n    return\n  }\n%s}\n'
            % (i, ind(body(p), 4), p[0],
               dmp(p, '  TR.dump("%s")\n' % p[0])))
        for g in range(0, n, 100):
            src += "fun d%d(i: Int) {\n  when (i) {\n" % (g // 100)
            for i in range(g, min(g + 100, n)):
                src += "    %d -> pr%d()\n" % (i, i)
            src += "  }\n}\n"
        src += "fun run(i: Int) {\n  when (i / 100) {\n"
        for g in range(0, n, 100):
            src += "    %d -> d%d(i)\n" % (g // 100, g // 100)
        src += "  }\n}\n"
        src += ('fun main(args: Array<String>) {\n  val s = if'
                ' (args.isNotEmpty()) args[0].toInt() else 0\n'
                '  for (i in s until %d) run(i)\n'
                '  println("__END__")\n}\n' % n)
        return src, "Chunk.kt"

    if lang == "swift":
        src = rt + "\n" + tr + "\n" + "\n".join(pres) + "\n"
        src += marked(lambda i, p:
            'func pr%d() {\n%s%s}\n'
            % (i, ind(body(p), 2),
               dmp(p, '  _dump("%s")\n' % p[0])))
        src += "let _P: [() -> Void] = [\n"
        src += "".join("  pr%d,\n" % i for i in range(n))
        src += "]\nsetvbuf(stdout, nil, _IONBF, 0)\nvar _s = 0\n"
        src += ("if CommandLine.arguments.count > 1 "
                "{ _s = Int(CommandLine.arguments[1]) ?? 0 }\n")
        src += "var _i = _s\nwhile _i < _P.count {\n  _P[_i]()\n  _i += 1\n}\n"
        src += 'print("__END__")\n'
        return src, "main.swift"

    raise SystemExit("no builder for " + lang)
'''


def wrap64(s, n=76):
    return "\n".join(s[i:i + n] for i in range(0, len(s), n))


def b64(s):
    return wrap64(base64.b64encode(s.encode("utf-8")).decode("ascii"))


def gz64(s):
    return wrap64(base64.b64encode(
        gzip.compress(s.encode("utf-8"), 9)).decode("ascii"))


LANE = r'''#!/bin/sh
# layer-3 CONSTRUCT lane -- %(LANG)s -- generated by
# l3_construct_lang.py.  Design: construct_design.md (2026-08-19).
# Stage A acceptance: %(ROUTE)s.  Stage B execution: chunks of %(CH)d,
# one compile each, the binary takes a start index.
# %(N)d acceptance probes.
set -u
export HOME=/work
export GO111MODULE=off
export GOCACHE=/work/.gocache
export GOPATH=/work/.gopath
export PATH=/persist/dart-sdk/bin:/persist/dotnet:$PATH
if [ -f /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 ]; then
  ln -sf /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 \
     /usr/lib/x86_64-linux-gnu/libncurses.so.6 2>/dev/null
  ldconfig 2>/dev/null
fi
ROOT=/work/kx_%(LANG)s
rm -rf "$ROOT"; mkdir -p "$ROOT"
echo "=== layer-3 CONSTRUCTS -- %(LANG)s -- %(N)d acceptance probes ==="
date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ
df -Pm /work | awk 'NR==2{print "scratch check: free /work " $4 " MB"}'
FREE=`df -Pm /work | awk 'NR==2{print $4}'`
if [ "$FREE" -lt 400 ]; then
  echo "!! REFUSING TO START: only $FREE MB free on /work, need 400"
  exit 3
fi
base64 -d <<'B64_EOF' | gunzip > "$ROOT/probes.jsonl"
%(PROBES)s
B64_EOF
base64 -d <<'B64_EOF' | gunzip > "$ROOT/rt.txt"
%(RT)s
B64_EOF
base64 -d <<'B64_EOF' | gunzip > "$ROOT/tr.txt"
%(TR)s
B64_EOF
%(AUX)s
base64 -d <<'PY_EOF' | gunzip > "$ROOT/drv.py"
%(DRV)s
PY_EOF
python3 "$ROOT/drv.py" "$ROOT"
echo "=== constructs %(LANG)s done ==="
date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ
'''

DRV = r'''
import glob
import json
import os
import re as _re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

ROOT = sys.argv[1]
LANG = "{LANG}"
EXT = "{EXT}"
CH = {CH}
CAP = 3000.0
PROBES = [json.loads(l) for l in open(os.path.join(ROOT, "probes.jsonl"))]
RTX = open(os.path.join(ROOT, "rt.txt")).read()
TRX = open(os.path.join(ROOT, "tr.txt")).read()
ACC_OUT = open("/out/kx_{LANG}.txt", "w")
ANS_OUT = open("/out/ky_{LANG}.txt", "w")
N = len(PROBES)
DOT = "/persist/dotnet"

{SRCGEN}


def hms(x):
    if x is None or x < 0:
        return "--:--:--"
    x = int(x)
    return "%02d:%02d:%02d" % (x // 3600, (x % 3600) // 60, x % 60)


def free_mb(p="/work"):
    st = os.statvfs(p)
    return st.f_bavail * st.f_frsize // (1024 * 1024)


def tup(p):
    return (p["id"], p["cons"], p["pres"], p["decls"], p["body"])


print("CONSTRUCTS {LANG}: %d acceptance probes, route {ROUTE}" % N)
print("scratch: %d MB free on /work" % free_mb())
sys.stdout.flush()

# ------------------------------------------------------ stage A: accept
SRC = os.path.join(ROOT, "src")
os.makedirs(SRC, exist_ok=True)
NAMES = []
for k, p in enumerate(PROBES):
    nm = "p%05d" % k
    NAMES.append(nm)
    s, _f = one(LANG, RTX, TRX, tup(p))
    open(os.path.join(SRC, nm + "." + EXT), "w").write(s)
print("stage A: %d sources written" % N)
sys.stdout.flush()

verdict = {}
tA = time.time()
done = [0]


def note(k):
    done[0] += 1
    if done[0] % max(50, N // 40) == 0:
        el = time.time() - tA
        print("[progress] {LANG} accept [%d/%d] %5.1f%%  elapsed %s"
              "  ETA %s  mean %.1f ms"
              % (done[0], N, 100.0 * done[0] / N, hms(el),
                 hms(el / done[0] * (N - done[0])), 1000.0 * el / done[0]))
        sys.stdout.flush()


MODE = "{AMODE}"

if MODE == "perfile":
    CMD = {
      "rust": lambda f: ["rustc", "--emit=metadata", "-o",
                         f.replace(".rs", ".rmeta"), f],
      "cpp": lambda f: ["g++", "-std=c++20", "-fsyntax-only", f],
      # the FULL swift compiler, never -typecheck (log 034).
      "swift": lambda f: ["/persist/swift/usr/bin/swiftc", "-Onone",
                          "-suppress-warnings", "-o", f + ".bin", f],
    }[LANG]

    def work(k):
        f = os.path.join(SRC, NAMES[k] + "." + EXT)
        try:
            r = subprocess.run(CMD(f), capture_output=True, text=True,
                               cwd=ROOT, timeout=120)
            rc, err = r.returncode, (r.stderr or "")[:300]
        except Exception as e:
            rc, err = 99, "HARNESS:%s" % e
        return k, ("ACCEPT" if rc == 0 else "REFUSE"), err

    with ThreadPoolExecutor(max_workers=(os.cpu_count() or 4)) as ex:
        for k, v, d in ex.map(work, range(N)):
            verdict[k] = (v, d)
            note(k)

elif MODE == "dart":
    DART = "/persist/dart-sdk/bin/dart"
    STEP = 400
    for i in range(0, N, STEP):
        d = os.path.join(ROOT, "an")
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        for k in range(i, min(i + STEP, N)):
            shutil.copy(os.path.join(SRC, NAMES[k] + ".dart"), d)
        r = subprocess.run([DART, "analyze", "--format=machine", "."],
                           capture_output=True, text=True, cwd=d)
        bad = {}
        for line in (r.stdout or "").splitlines() + (r.stderr or "").splitlines():
            f = line.split("|")
            # SEVERITY|TYPE|CODE|FILE|LINE|COL|LEN|MESSAGE.  ONLY severity
            # ERROR is a refusal: a dart LINT (dead_code and friends) is
            # not the language refusing the probe.  log 030's fix.
            if len(f) >= 8 and f[0] == "ERROR":
                b = os.path.basename(f[3]).replace(".dart", "")
                bad.setdefault(b, f[7][:200])
        for k in range(i, min(i + STEP, N)):
            nm = NAMES[k]
            verdict[k] = (("REFUSE", bad[nm]) if nm in bad
                          else ("ACCEPT", ""))
            note(k)

else:                      # in-process: csharp, java, kotlin, typescript
    drv = os.path.join(ROOT, "drv")
    os.makedirs(drv, exist_ok=True)
    lst = os.path.join(drv, "list.txt")
    open(lst, "w").write("\n".join(
        os.path.join(SRC, nm + "." + EXT) for nm in NAMES))
    if LANG == "csharp":
        REF = sorted(glob.glob(
            DOT + "/packs/Microsoft.NETCore.App.Ref/*/ref/net*"))[-1]
        CSC = sorted(glob.glob(DOT + "/sdk/*/Roslyn/bincore/csc.dll"))[-1]
        BIN = os.path.dirname(CSC)
        open(os.path.join(drv, "Drv.cs"), "w").write(
            open(os.path.join(ROOT, "aux.txt")).read())
        refs = ["-reference:" + os.path.join(REF, f)
                for f in os.listdir(REF) if f.endswith(".dll")]
        refs += ["-reference:" + os.path.join(BIN, n)
                 for n in ("Microsoft.CodeAnalysis.dll",
                           "Microsoft.CodeAnalysis.CSharp.dll")]
        r = subprocess.run([DOT + "/dotnet", "exec", CSC, "-nologo",
                            "-out:Drv.dll", "-target:exe"] + refs
                           + ["Drv.cs"], capture_output=True, text=True,
                           cwd=drv)
        print("driver build rc=%d %s" % (r.returncode, (r.stdout or "")[:300]))
        for nm in os.listdir(BIN):
            if nm.startswith("Microsoft.CodeAnalysis") or nm.startswith("System."):
                try:
                    shutil.copy(os.path.join(BIN, nm), drv)
                except Exception:
                    pass
        ver = REF.split("/")[-3]
        tfm = REF.split("/")[-1]
        open(os.path.join(drv, "Drv.runtimeconfig.json"), "w").write(
            '{"runtimeOptions":{"tfm":"%s","framework":{"name":'
            '"Microsoft.NETCore.App","version":"%s"}}}' % (tfm, ver))
        argv = [DOT + "/dotnet", "Drv.dll", REF, lst]
    elif LANG == "java":
        open(os.path.join(drv, "JDrv.java"), "w").write(
            open(os.path.join(ROOT, "aux.txt")).read())
        r = subprocess.run(["javac", "JDrv.java"], capture_output=True,
                           text=True, cwd=drv)
        print("driver build rc=%d %s" % (r.returncode, (r.stderr or "")[:300]))
        argv = ["java", "-cp", ".", "JDrv", lst]
    elif LANG == "kotlin":
        JAR = "/persist/kotlinc/lib/kotlin-compiler.jar"
        open(os.path.join(drv, "KDrv.java"), "w").write(
            open(os.path.join(ROOT, "aux.txt")).read())
        r = subprocess.run(["javac", "-cp", JAR, "KDrv.java"],
                           capture_output=True, text=True, cwd=drv)
        print("driver build rc=%d %s" % (r.returncode, (r.stderr or "")[:300]))
        argv = ["java", "-cp", JAR + ":.", "KDrv", lst,
                os.path.join(ROOT, "kout")]
    else:
        open(os.path.join(drv, "tdrv.js"), "w").write(
            open(os.path.join(ROOT, "aux.txt")).read())
        argv = ["node", "--max-old-space-size=3000", "tdrv.js", lst]
    pos = {nm: k for k, nm in enumerate(NAMES)}
    pr = subprocess.Popen(argv, stdout=subprocess.PIPE, text=True, cwd=drv)
    for line in pr.stdout:
        line = line.strip()
        if "|" not in line:
            continue
        f, v = line.split("|", 1)
        if f.startswith("__"):
            print("inner " + line)
            sys.stdout.flush()
            continue
        nm = f.split(".")[0]
        if nm not in pos:
            continue
        if LANG == "kotlin":
            v = "ACCEPT" if v in ("OK", "0") else "REFUSE"
        verdict[pos[nm]] = (v if v in ("ACCEPT", "REFUSE") else "REFUSE", "")
        note(pos[nm])
    pr.wait()

elA = time.time() - tA
acc = [k for k in range(N) if verdict.get(k, ("REFUSE",))[0] == "ACCEPT"]
for k in range(N):
    v, d = verdict.get(k, ("MISSING", "no verdict row"))
    ACC_OUT.write("%s|%s|%s\n" % (PROBES[k]["id"], v,
                                  d.replace("\n", " ")[:200]))
ACC_OUT.write("__SUMMARY__|%d|%d|%d|%.3f\n"
              % (N, len(acc), N - len(acc), elA))
ACC_OUT.close()
print("== stage A {LANG}: %d probes, %d ACCEPT, %d REFUSE, %.1f s"
      % (N, len(acc), N - len(acc), elA))
sys.stdout.flush()

# --------------------------------------------------- stage B: execution
def build_cmds(lang, d, fname):
    if lang == "rust":
        return ([["rustc", "-C", "debug-assertions=on", "-C", "opt-level=0",
                  "-o", d + "/bin", d + "/" + fname]],
                lambda s: [d + "/bin", str(s)])
    if lang == "cpp":
        return ([["g++", "-std=c++20", "-O0", "-w", "-o", d + "/bin",
                  d + "/" + fname]], lambda s: [d + "/bin", str(s)])
    if lang == "swift":
        return ([["/persist/swift/usr/bin/swiftc", "-Onone",
                  "-suppress-warnings", "-o", d + "/bin", d + "/" + fname]],
                lambda s: [d + "/bin", str(s)])
    if lang == "dart":
        return ([["/persist/dart-sdk/bin/dart", "compile", "exe",
                  d + "/" + fname, "-o", d + "/bin"]],
                lambda s: [d + "/bin", str(s)])
    if lang == "java":
        return ([["javac", "-nowarn", "-d", d + "/cls", d + "/" + fname]],
                lambda s: ["java", "-cp", d + "/cls", "Chunk", str(s)])
    if lang == "kotlin":
        std = "/persist/kotlinc/lib/kotlin-stdlib.jar"
        return ([["/persist/kotlinc/bin/kotlinc", "-nowarn", "-d",
                  d + "/cls", d + "/" + fname]],
                lambda s: ["java", "-cp", d + "/cls:" + std, "ChunkKt",
                           str(s)])
    if lang == "csharp":
        refd = sorted(glob.glob(
            DOT + "/packs/Microsoft.NETCore.App.Ref/*/ref/net*"))[-1]
        csc = sorted(glob.glob(DOT + "/sdk/*/Roslyn/bincore/csc.dll"))[-1]
        open(d + "/Chunk.runtimeconfig.json", "w").write(
            '{"runtimeOptions":{"tfm":"%s","framework":{"name":'
            '"Microsoft.NETCore.App","version":"%s"}}}'
            % (refd.split("/")[-1], refd.split("/")[-3]))
        refs = ["-reference:" + os.path.join(refd, f)
                for f in os.listdir(refd) if f.endswith(".dll")]
        return ([[DOT + "/dotnet", "exec", csc, "-nologo",
                  "-out:" + d + "/Chunk.dll", "-target:exe"] + refs
                 + [d + "/" + fname]],
                lambda s: [DOT + "/dotnet", d + "/Chunk.dll", str(s)])
    if lang == "typescript":
        tsc = "/persist/tv/ts5/node_modules/typescript/lib/typescript.js"
        open(d + "/tr.js", "w").write(
            "const ts=require(%r);const fs=require('fs');"
            "const src=fs.readFileSync(process.argv[2],'utf8');"
            "const o=ts.transpileModule(src,{compilerOptions:"
            "{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS}});"
            "fs.writeFileSync(process.argv[3],o.outputText);" % tsc)
        return ([["node", d + "/tr.js", d + "/" + fname, d + "/chunk.js"]],
                lambda s: ["node", "--stack-size=4000", d + "/chunk.js",
                           str(s)])
    raise SystemExit("no toolchain for " + lang)


def probe_spans(src):
    """line number -> probe id, from the __PROBE__ markers."""
    spans = []
    for n, line in enumerate(src.splitlines(), 1):
        m = _re.search(r"__PROBE__ (\S+)", line)
        if m:
            spans.append((n, m.group(1)))
    return spans


def map_errors(msg, spans):
    bad = set()
    for m in _re.finditer(r"[:(](\d+)[:,)]", msg):
        ln = int(m.group(1))
        cur = None
        for n, pid in spans:
            if n <= ln:
                cur = pid
            else:
                break
        if cur and cur != "-":
            bad.add(cur)
    return bad


rows = [tup(PROBES[k]) for k in acc]
chunks = [rows[i:i + CH] for i in range(0, len(rows), CH)]
tB = time.time()
nans = nraise = ndeath = ncgr = 0
seen = 0
print("stage B: %d accepted probes, %d chunks of %d"
      % (len(rows), len(chunks), CH))
sys.stdout.flush()

for ci, rws in enumerate(chunks):
    if time.time() - tB > CAP:
        print("!! TIME CAP reached before chunk %d" % ci)
        break
    if free_mb() < 300:
        print("!! SCRATCH LOW (%d MB) -- stopping before chunk %d"
              % (free_mb(), ci))
        break
    d = os.path.join(ROOT, "c%03d" % ci)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    probes = list(rws)
    ok = False
    for attempt in range(12):
        if not probes:
            break
        src, fname = chunk(LANG, RTX, TRX, probes)
        open(os.path.join(d, fname), "w").write(src)
        spans = probe_spans(src)
        cmds, runf = build_cmds(LANG, d, fname)
        ok, msg = True, ""
        for c in cmds:
            try:
                r = subprocess.run(c, capture_output=True, text=True,
                                   cwd=d, timeout=1800)
            except Exception as e:
                ok, msg = False, "HARNESS:%s" % e
                break
            if r.returncode != 0:
                ok, msg = False, (r.stderr or "") + "\n" + (r.stdout or "")
                break
        if ok:
            break
        bad = map_errors(msg, spans)
        print("!! chunk %d compile attempt %d failed; %d probes named"
              % (ci, attempt, len(bad)))
        sys.stdout.flush()
        if not bad:
            open("/out/ky_{LANG}.compilefail.%d.txt" % ci, "w").write(
                msg[:200000])
            break
        for pid in bad:
            ANS_OUT.write("%s|-|CODEGEN_REFUSE:%s\n"
                          % (pid, msg.replace("\n", " ")[:160]))
            ncgr += 1
        probes = [p for p in probes if p[0] not in bad]
    if not ok or not probes:
        continue
    ids = [p[0] for p in probes]
    start = 0
    while start < len(probes):
        try:
            r = subprocess.run(runf(start), capture_output=True, text=True,
                               cwd=d, timeout=600)
            out = r.stdout or ""
        except Exception:
            out = ""
            r = None
        got = set()
        for line in out.splitlines():
            if line.strip() == "__END__":
                continue
            if line.count("|") >= 2:
                ANS_OUT.write(line + "\n")
                got.add(line.split("|", 1)[0])
                if "|-|RAISE" in line:
                    nraise += 1
                else:
                    nans += 1
        nxt = start
        while nxt < len(probes) and ids[nxt] in got:
            nxt += 1
        if out.rstrip().endswith("__END__") or nxt >= len(probes):
            start = len(probes)
        else:
            # the process died where the language could not catch it.
            # The binary takes a start index, so the death costs exactly
            # one probe and the lane restarts past the corpse.
            rc = r.returncode if r is not None else -1
            ANS_OUT.write("%s|-|DEATH:%d\n" % (ids[nxt], rc))
            ndeath += 1
            start = nxt + 1
    ANS_OUT.flush()
    seen += len(probes)
    el = time.time() - tB
    print("[progress] {LANG} exec chunk [%d/%d] probes %d/%d  elapsed %s"
          "  ETA %s  free %d MB"
          % (ci + 1, len(chunks), seen, len(rows), hms(el),
             hms(el / (ci + 1) * (len(chunks) - ci - 1)), free_mb()))
    sys.stdout.flush()
    shutil.rmtree(d, ignore_errors=True)

elB = time.time() - tB
ANS_OUT.write("__SUMMARY__|%d|%d|%d|%.3f\n"
              % (len(rows), nans, nraise + ndeath + ncgr, elB))
ANS_OUT.close()
print("== stage B {LANG}: %d accepted, %d answer/trace rows, %d raises,"
      " %d deaths, %d codegen refusals, %.1f s"
      % (len(rows), nans, nraise, ndeath, ncgr, elB))
'''

ROUTE = dict(
    typescript="A1 shipped typescript.js Program diagnostics",
    csharp="A1 Roslyn CSharpCompilation.GetDiagnostics in-process",
    rust="A2 rustc --emit=metadata per file",
    cpp="A2 g++ -std=c++20 -fsyntax-only per file",
    dart="A2 dart analyze --format=machine, severity ERROR only",
    java="A1 javax.tools JavacTask.analyze in-process, one JVM",
    swift="A2 the FULL swiftc, never -typecheck",
    kotlin="A1 K2JVMCompiler in a warm JVM, in-process",
)
AMODE = dict(typescript="inproc", csharp="inproc", rust="perfile",
             cpp="perfile", dart="dart", java="inproc", swift="perfile",
             kotlin="inproc")
AUXDRV = dict(typescript=TDRV_JS, csharp=DRV_CS, java=JDRV_JAVA,
              kotlin=KDRV_JAVA)


def emit(lang):
    probes = gen_probes(lang)
    cap = int(os.environ.get("CONSTRUCT_CAP", "0"))
    if cap:
        # a SMOKE subset: a spread across every construct, so that a
        # cheap run proves the scaffolds compile before the full lane
        # pays for them.  Never used for a measured run.
        byc = {}
        for p in probes:
            byc.setdefault(p[1], []).append(p)
        probes = []
        for c in sorted(byc):
            xs = byc[c]
            step = max(1, len(xs) // max(1, cap // max(1, len(byc))))
            probes += xs[::step][:cap]
    jl = "\n".join(json.dumps(dict(id=p[0], cons=p[1], pres=p[2],
                                   decls=p[3], body=p[4]))
                   for p in probes)
    drv = (DRV.replace("{SRCGEN}", SRCGEN)
              .replace("{LANG}", lang)
              .replace("{EXT}", EXT[lang])
              .replace("{CH}", str(CHUNK[lang]))
              .replace("{ROUTE}", ROUTE[lang])
              .replace("{AMODE}", AMODE[lang]))
    aux = ""
    if lang in AUXDRV:
        aux = ("base64 -d <<'B64_EOF' | gunzip > \"$ROOT/aux.txt\"\n%s\n"
               "B64_EOF" % gz64(AUXDRV[lang]))
    sh = LANE % dict(LANG=lang, N=len(probes), CH=CHUNK[lang],
                     ROUTE=ROUTE[lang], PROBES=gz64(jl),
                     RT=gz64(RT[lang]), TR=gz64(TRACE[lang]),
                     AUX=aux, DRV=gz64(drv))
    p = os.path.join(LANES, "kx_%s.sh" % lang)
    open(p, "w").write(sh)
    os.chmod(p, 0o755)
    hs, _ = holders(lang)
    mp = os.path.join(HERE, "manifest_construct_%s.json" % lang)
    per = {}
    for pr in probes:
        per[pr[1]] = per.get(pr[1], 0) + 1
    json.dump(dict(language=lang, frozen="2026-08-19",
                   design="construct_design.md",
                   route_acceptance=ROUTE[lang],
                   holders=[dict(i=n, form=h["form"], rep=h["rep"],
                                 value_classes=sorted(h["values"]))
                            for n, h in enumerate(hs)],
                   not_applicable=NOT_APPLICABLE.get(lang, {}),
                   constructs_probed=per,
                   scaffolds=SCAF[lang],
                   aug_ops=AUG_OPS, jump_k=JUMP_K,
                   chunk=CHUNK[lang],
                   acceptance_probes=len(probes)),
              open(mp, "w"), indent=1)
    return len(probes), p, per


def main():
    which = sys.argv[1:] or LANGS
    print("layer-3 CONSTRUCT lanes -- derived counts, printed before "
          "anything runs")
    print("")
    tot = 0
    for lang in which:
        n, p, per = emit(lang)
        tot += n
        print("  %-11s %5d acceptance probes  ->  %s"
              % (lang, n, os.path.basename(p)))
        for c in sorted(per):
            print("      %-20s %5d" % (c, per[c]))
    print("")
    print("  TOTAL %d acceptance probes over %d languages"
          % (tot, len(which)))


if __name__ == "__main__":
    main()
