#!/usr/bin/env python3
"""l3_exec.py -- LAYER 3, EXECUTION: what the accepted operations RETURN.

The acceptance grain and the value matrix both measure VERDICTS.  This
file measures ANSWERS, for the nine statically checked languages, and it
does so on the one set where batching is safe: the probes the value
matrix already recorded as ACCEPT.  Those are known to compile, so a
file holding many of them holds no compile failure by construction, and
there is nothing to bisect.

Design, ruled in conversation 2026-08-18 and built here.

  * SINGLE-FILE COMPILATION.  Accepted probes are emitted as one
    function each into a small number of CHUNK files per language.  One
    compile per chunk instead of one per probe.
  * BITS AND TYPE.  Every answer records the language's OWN result type
    name and the raw content: integers as two's-complement bytes,
    floats as IEEE bit patterns, text as its byte length plus hex bytes
    plus the language's own length notion, containers recursively in
    the same encoding.  Nothing is canonicalised at run time; the
    comparison happens at read time, over the recorded bits.
  * DEATH IS SURVIVABLE.  Where the language can catch a runtime raise
    the probe is wrapped and every probe yields a line.  Where it
    cannot (a c++ SIGFPE, a swift trap) the chunk binary takes a START
    INDEX and the runner restarts it past the corpse, so a death costs
    ONE probe and not a chunk.

Line format, one per probe:

    PROBE_ID|TYPE_NAME|ENCODING:PAYLOAD
    PROBE_ID|-|RAISE:<name>
    PROBE_ID|-|DEATH:<signal or rc>

Probe ids are the value matrix's own ids, P<i>_<j>_<x>_<y>_<k>, so an
answer row joins to its verdict row by id and nothing has to be
re-derived.
"""

import base64
import gzip
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.join(HERE, "lanes")
RAW = os.path.join(HERE, "raw")
os.makedirs(LANES, exist_ok=True)
sys.path.insert(0, HERE)
from l3_accept import LANG, holders, ops                    # noqa: E402
from l3_lanes import EXT                                    # noqa: E402

LANGS = ["go", "rust", "cpp", "java", "csharp", "typescript", "swift",
         "kotlin", "dart"]

# probes per chunk.  Chosen against the compiler's own habits: swift's
# type checker is superlinear in a file's size, kotlin and java carry a
# 64 KB method limit that the dispatch tables respect, everything else
# is bounded by how much of a chunk one uncatchable death would cost.
CHUNK = dict(go=1500, rust=1500, cpp=2000, java=2000, csharp=2000,
             typescript=5000, swift=400, kotlin=2000, dart=3000)

# can the language catch a runtime death IN LANGUAGE?
CATCHABLE = dict(go=True, rust=True, cpp="partly", java=True, csharp=True,
                 typescript=True, swift=False, kotlin=True, dart=True)


# ---------------------------------------------------------------- accepted

def accepted(lang):
    """the ACCEPT ids of the value matrix, in id order, as tuples."""
    ids = []
    n = 0
    for fn in sorted(os.listdir(RAW)):
        if not fn.startswith("vm_%s_" % lang) or not fn.endswith(".txt"):
            continue
        for line in open(os.path.join(RAW, fn)):
            if "|ACCEPT|" not in line:
                continue
            pid = line.split("|", 1)[0]
            if not pid.startswith("P"):
                continue
            t = tuple(int(z) for z in pid[1:].split("_"))
            ids.append(t)
            n += 1
    ids.sort()
    return ids


def table(lang):
    hs = holders(lang)[0]
    os_ = ops(lang)
    tpl = LANG[lang]
    return dict(language=lang, ops=os_, ext=EXT[lang],
                holders=[dict(form=h["form"], rep=h["rep"],
                              pre=h.get("pre", ""),
                              values=[[k, h["values"][k]]
                                      for k in sorted(h["values"])])
                         for h in hs])


# ------------------------------------------------------------- lane pieces
# The lane assembles its own sources: the rule that builds `da`, `db`
# and the hoisted pre-lines is the value matrix's rule, copied
# unchanged, because the probes were ACCEPTED under exactly it.

ASSEMBLE = r'''
import re as _re

_DT = _re.compile(r"\b(?:record|class|interface|enum)\s+([A-Za-z_]\w*)")

def _rn(s, n):
    return _re.sub(r"\bv\b", n, s)

def _side(decl, suffix):
    for n in sorted(set(_DT.findall(decl)), key=len, reverse=True):
        decl = _re.sub(r"\b%s\b" % _re.escape(n), n + suffix, decl)
    return decl

def assemble(T, rows):
    """(probe id, function name, pre lines, decl a, decl b, op) per row."""
    HS, OPS, L = T["holders"], T["ops"], T["language"]
    out = []
    for (i, j, x, y, k) in rows:
        ha, hb = HS[i], HS[j]
        da = _rn(ha["values"][x][1], "a")
        db = _rn(hb["values"][y][1], "b")
        if L == "java":
            db = _side(db, "_b")
        pres = []
        for h, dtext in ((ha, da), (hb, db)):
            for line in (h.get("pre") or "").splitlines():
                line = line.strip()
                if not line:
                    continue
                m = _re.findall(r"[A-Za-z_][A-Za-z_0-9]*", line)
                tok = m[-1] if m else ""
                if L in ("go", "rust") and tok and tok not in dtext:
                    continue
                if line not in pres:
                    pres.append(line)
        ident = "%d_%d_%d_%d_%d" % (i, j, x, y, k)
        out.append(("P" + ident, "p_" + ident, pres, da, db, OPS[k]))
    return out
'''

# ------------------------------------------------------------- the runtimes

RT_GO = r'''
var _W = bufio.NewWriterSize(os.Stdout, 1<<14)

func _hx(b []byte) string {
	const h = "0123456789abcdef"
	s := make([]byte, 0, len(b)*2)
	for _, c := range b {
		s = append(s, h[c>>4], h[c&15])
	}
	return string(s)
}

func _ih(u uint64, bits int) string {
	s := strconv.FormatUint(u, 16)
	n := bits / 4
	for len(s) < n {
		s = "0" + s
	}
	if len(s) > n {
		s = s[len(s)-n:]
	}
	return s
}

func _enc(rv reflect.Value) string {
	if !rv.IsValid() {
		return "NULL"
	}
	switch rv.Kind() {
	case reflect.Interface, reflect.Pointer:
		if rv.IsNil() {
			return "NULL"
		}
		return "REF(" + _enc(rv.Elem()) + ")"
	case reflect.Bool:
		if rv.Bool() {
			return "BOOL:true"
		}
		return "BOOL:false"
	case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32,
		reflect.Int64:
		b := rv.Type().Bits()
		return fmt.Sprintf("INT:%d:%s", b, _ih(uint64(rv.Int()), b))
	case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32,
		reflect.Uint64, reflect.Uintptr:
		b := rv.Type().Bits()
		return fmt.Sprintf("UINT:%d:%s", b, _ih(rv.Uint(), b))
	case reflect.Float32:
		return "FLOAT:32:" + _ih(uint64(math.Float32bits(float32(rv.Float()))), 32)
	case reflect.Float64:
		return "FLOAT:64:" + _ih(math.Float64bits(rv.Float()), 64)
	case reflect.String:
		s := rv.String()
		return fmt.Sprintf("STR:%d:%d:%s", len(s), len(s), _hx([]byte(s)))
	case reflect.Slice, reflect.Array:
		if rv.Kind() == reflect.Slice && rv.IsNil() {
			return "NULL"
		}
		ps := make([]string, 0, rv.Len())
		for i := 0; i < rv.Len(); i++ {
			ps = append(ps, _enc(rv.Index(i)))
		}
		return fmt.Sprintf("LIST:%d[%s]", rv.Len(), strings.Join(ps, ","))
	case reflect.Map:
		ps := make([]string, 0, rv.Len())
		it := rv.MapRange()
		for it.Next() {
			ps = append(ps, _enc(it.Key())+"=>"+_enc(it.Value()))
		}
		sort.Strings(ps)
		return fmt.Sprintf("MAP:%d[%s]", rv.Len(), strings.Join(ps, ","))
	case reflect.Struct:
		t := rv.Type()
		ps := make([]string, 0, rv.NumField())
		for i := 0; i < rv.NumField(); i++ {
			if !rv.Field(i).CanInterface() {
				ps = append(ps, t.Field(i).Name+"=OPAQUE:")
				continue
			}
			ps = append(ps, t.Field(i).Name+"="+_enc(rv.Field(i)))
		}
		return fmt.Sprintf("STRUCT:%d[%s]", rv.NumField(), strings.Join(ps, ","))
	}
	return "OPAQUE:" + _hx([]byte(fmt.Sprint(rv)))
}

func _emit(id string, v interface{}) {
	tn := "nil"
	if v != nil {
		tn = reflect.TypeOf(v).String()
	}
	fmt.Fprintf(_W, "%s|%s|%s\n", id, tn, _enc(reflect.ValueOf(v)))
	_W.Flush()
}

func _guard(id string) {
	if r := recover(); r != nil {
		fmt.Fprintf(_W, "%s|-|RAISE:%v\n", id, r)
		_W.Flush()
	}
}
'''

RT_RUST = r'''
fn _hx(b: &[u8]) -> String {
    let mut s = String::with_capacity(b.len() * 2);
    for c in b { s.push_str(&format!("{:02x}", c)); }
    s
}

pub trait DB { fn db(&self) -> String; }

macro_rules! _dbi {
    ($($t:ty => $b:expr),* $(,)?) => { $(
        impl DB for $t {
            fn db(&self) -> String {
                format!("INT:{}:{}", $b, _hx(&self.to_be_bytes()))
            }
        })* }
}
macro_rules! _dbu {
    ($($t:ty => $b:expr),* $(,)?) => { $(
        impl DB for $t {
            fn db(&self) -> String {
                format!("UINT:{}:{}", $b, _hx(&self.to_be_bytes()))
            }
        })* }
}
_dbi!(i8=>8, i16=>16, i32=>32, i64=>64, i128=>128, isize=>64);
_dbu!(u8=>8, u16=>16, u32=>32, u64=>64, u128=>128, usize=>64);

impl DB for f32 {
    fn db(&self) -> String {
        format!("FLOAT:32:{}", _hx(&self.to_bits().to_be_bytes()))
    }
}
impl DB for f64 {
    fn db(&self) -> String {
        format!("FLOAT:64:{}", _hx(&self.to_bits().to_be_bytes()))
    }
}
impl DB for bool {
    fn db(&self) -> String {
        format!("BOOL:{}", if *self { "true" } else { "false" })
    }
}
impl DB for char {
    fn db(&self) -> String { format!("CHAR:{:x}", *self as u32) }
}
impl DB for str {
    fn db(&self) -> String {
        format!("STR:{}:{}:{}", self.chars().count(), self.len(),
                _hx(self.as_bytes()))
    }
}
impl DB for String {
    fn db(&self) -> String { self.as_str().db() }
}
impl DB for () {
    fn db(&self) -> String { String::from("UNIT") }
}
impl<T: DB + ?Sized> DB for &T {
    fn db(&self) -> String { (**self).db() }
}
impl<T: DB> DB for Vec<T> {
    fn db(&self) -> String { self.as_slice().db() }
}
impl<T: DB> DB for [T] {
    fn db(&self) -> String {
        let v: Vec<String> = self.iter().map(|e| e.db()).collect();
        format!("LIST:{}[{}]", self.len(), v.join(","))
    }
}
impl<T: DB, const N: usize> DB for [T; N] {
    fn db(&self) -> String { self.as_slice().db() }
}
impl<T: DB> DB for Option<T> {
    fn db(&self) -> String {
        match self { None => String::from("NULL"),
                     Some(x) => format!("SOME({})", x.db()) }
    }
}
impl<T: DB> DB for std::ops::Range<T> {
    fn db(&self) -> String {
        format!("RANGE[{},{},excl]", self.start.db(), self.end.db())
    }
}
impl<T: DB> DB for std::ops::RangeInclusive<T> {
    fn db(&self) -> String {
        format!("RANGE[{},{},incl]", self.start().db(), self.end().db())
    }
}
impl<T: DB> DB for std::collections::VecDeque<T> {
    fn db(&self) -> String {
        let v: Vec<String> = self.iter().map(|e| e.db()).collect();
        format!("LIST:{}[{}]", self.len(), v.join(","))
    }
}
impl<K: DB, V: DB> DB for std::collections::BTreeMap<K, V> {
    fn db(&self) -> String {
        let mut v: Vec<String> =
            self.iter().map(|(k, x)| format!("{}=>{}", k.db(), x.db())).collect();
        v.sort();
        format!("MAP:{}[{}]", self.len(), v.join(","))
    }
}
impl<K: DB, V: DB> DB for std::collections::HashMap<K, V> {
    fn db(&self) -> String {
        let mut v: Vec<String> =
            self.iter().map(|(k, x)| format!("{}=>{}", k.db(), x.db())).collect();
        v.sort();
        format!("MAP:{}[{}]", self.len(), v.join(","))
    }
}
macro_rules! _dbt {
    ($(($($n:tt : $t:ident),+)),* $(,)?) => { $(
        impl<$($t: DB),+> DB for ($($t,)+) {
            fn db(&self) -> String {
                let v: Vec<String> = vec![$(self.$n.db()),+];
                format!("TUP:{}[{}]", v.len(), v.join(","))
            }
        })* }
}
_dbt!((0:A), (0:A,1:B), (0:A,1:B,2:C), (0:A,1:B,2:C,3:D),
      (0:A,1:B,2:C,3:D,4:E), (0:A,1:B,2:C,3:D,4:E,5:F));

fn _emit<T: DB + ?Sized>(id: &str, v: &T) {
    use std::io::Write;
    let so = std::io::stdout();
    let mut o = so.lock();
    let _ = writeln!(o, "{}|{}|{}", id, std::any::type_name::<T>(), v.db());
    let _ = o.flush();
}
'''

RT_CPP = r'''
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <type_traits>
#include <typeinfo>
#include <compare>
#include <cxxabi.h>

static std::string _hxb(const unsigned char *p, size_t n) {
  static const char *h = "0123456789abcdef";
  std::string s;
  for (size_t i = 0; i < n; i++) { s += h[p[i] >> 4]; s += h[p[i] & 15]; }
  return s;
}
template <class T> static std::string _bits(const T &v) {
  unsigned char raw[sizeof(T)], be[sizeof(T)];
  std::memcpy(raw, &v, sizeof(T));
  for (size_t i = 0; i < sizeof(T); i++) be[i] = raw[sizeof(T) - 1 - i];
  return _hxb(be, sizeof(T));
}
static std::string _hxs(const std::string &s) {
  return _hxb((const unsigned char *)s.data(), s.size());
}
template <class T> static std::string _tn() {
  int st = 0;
  char *d = abi::__cxa_demangle(typeid(T).name(), 0, 0, &st);
  std::string r = d ? d : typeid(T).name();
  if (d) free(d);
  return r;
}
template <class T, class = void> struct _iter : std::false_type {};
template <class T>
struct _iter<T, std::void_t<decltype(std::begin(std::declval<const T &>())),
                            decltype(std::end(std::declval<const T &>()))>>
    : std::true_type {};

template <class T> std::string _enc(const T &v);

template <class T> std::string _enc(const T &v) {
  if constexpr (std::is_same_v<T, bool>) {
    return v ? "BOOL:true" : "BOOL:false";
  } else if constexpr (std::is_same_v<T, __int128>) {
    return "INT:128:" + _bits(v);
  } else if constexpr (std::is_same_v<T, unsigned __int128>) {
    return "UINT:128:" + _bits(v);
  } else if constexpr (std::is_integral_v<T>) {
    return (std::is_signed_v<T> ? "INT:" : "UINT:") +
           std::to_string(sizeof(T) * 8) + ":" + _bits(v);
  } else if constexpr (std::is_enum_v<T>) {
    return "ENUM:" + std::to_string((long long)v);
  } else if constexpr (std::is_floating_point_v<T>) {
    return "FLOAT:" + std::to_string(sizeof(T) * 8) + ":" + _bits(v);
  } else if constexpr (std::is_same_v<T, std::strong_ordering> ||
                       std::is_same_v<T, std::weak_ordering>) {
    return v < 0 ? "ORD:LT" : (v == 0 ? "ORD:EQ" : "ORD:GT");
  } else if constexpr (std::is_same_v<T, std::partial_ordering>) {
    if (v == std::partial_ordering::unordered) return "ORD:UN";
    return v < 0 ? "ORD:LT" : (v == 0 ? "ORD:EQ" : "ORD:GT");
  } else if constexpr (std::is_same_v<T, std::string>) {
    return "STR:" + std::to_string(v.size()) + ":" +
           std::to_string(v.size()) + ":" + _hxs(v);
  } else if constexpr (std::is_same_v<T, const char *> ||
                       std::is_same_v<T, char *>) {
    if (!v) return "NULL";
    std::string s(v);
    return "STR:" + std::to_string(s.size()) + ":" +
           std::to_string(s.size()) + ":" + _hxs(s);
  } else if constexpr (std::is_same_v<T, std::nullptr_t>) {
    return "NULL";
  } else if constexpr (std::is_pointer_v<T>) {
    return v ? "PTR" : "NULL";
  } else if constexpr (_iter<T>::value) {
    std::string s;
    size_t n = 0;
    for (const auto &e : v) {
      if (n) s += ",";
      s += _enc(e);
      n++;
    }
    return "LIST:" + std::to_string(n) + "[" + s + "]";
  } else {
    return "OPAQUE:";
  }
}

template <class T> void _emit(const char *id, const T &v) {
  std::string s = id;
  s += "|"; s += _tn<T>(); s += "|"; s += _enc(v); s += "\n";
  fwrite(s.data(), 1, s.size(), stdout);
  fflush(stdout);
}
static void _raise(const char *id, const char *what) {
  printf("%s|-|RAISE:%s\n", id, what);
  fflush(stdout);
}
'''

RT_SWIFT = r'''
import Foundation

func _hx(_ b: [UInt8]) -> String {
    var s = ""
    for x in b { s += String(format: "%02x", x) }
    return s
}
func _be<T>(_ v: T) -> [UInt8] {
    var a = withUnsafeBytes(of: v) { Array($0) }
    a.reverse()
    return a
}
func _enc(_ v: Any) -> String {
    switch v {
    case let x as Bool: return "BOOL:\(x)"
    case let x as Int: return "INT:64:" + _hx(_be(x))
    case let x as Int8: return "INT:8:" + _hx(_be(x))
    case let x as Int16: return "INT:16:" + _hx(_be(x))
    case let x as Int32: return "INT:32:" + _hx(_be(x))
    case let x as Int64: return "INT:64:" + _hx(_be(x))
    case let x as UInt: return "UINT:64:" + _hx(_be(x))
    case let x as UInt8: return "UINT:8:" + _hx(_be(x))
    case let x as UInt16: return "UINT:16:" + _hx(_be(x))
    case let x as UInt32: return "UINT:32:" + _hx(_be(x))
    case let x as UInt64: return "UINT:64:" + _hx(_be(x))
    case let x as Double: return "FLOAT:64:" + _hx(_be(x.bitPattern))
    case let x as Float: return "FLOAT:32:" + _hx(_be(x.bitPattern))
    case let x as String:
        let u = Array(x.utf8)
        return "STR:\(x.count):\(u.count):" + _hx(u)
    case let x as Substring:
        let u = Array(String(x).utf8)
        return "STR:\(x.count):\(u.count):" + _hx(u)
    case let x as Character:
        let u = Array(String(x).utf8)
        return "STR:1:\(u.count):" + _hx(u)
    default: break
    }
    let m = Mirror(reflecting: v)
    switch m.displayStyle {
    case .some(.optional):
        if let c = m.children.first { return "SOME(" + _enc(c.value) + ")" }
        return "NULL"
    case .some(.collection), .some(.set):
        var ps: [String] = []
        for c in m.children { ps.append(_enc(c.value)) }
        if m.displayStyle == .some(.set) { ps.sort() }
        return "LIST:\(ps.count)[" + ps.joined(separator: ",") + "]"
    case .some(.dictionary):
        var ps: [String] = []
        for c in m.children {
            let mm = Mirror(reflecting: c.value)
            let kv = Array(mm.children)
            if kv.count == 2 {
                ps.append(_enc(kv[0].value) + "=>" + _enc(kv[1].value))
            }
        }
        ps.sort()
        return "MAP:\(ps.count)[" + ps.joined(separator: ",") + "]"
    case .some(.tuple):
        var ps: [String] = []
        for c in m.children { ps.append(_enc(c.value)) }
        return "TUP:\(ps.count)[" + ps.joined(separator: ",") + "]"
    case .some(.struct), .some(.class):
        var ps: [String] = []
        for c in m.children {
            ps.append((c.label ?? "?") + "=" + _enc(c.value))
        }
        return "STRUCT:\(ps.count)[" + ps.joined(separator: ",") + "]"
    default:
        let u = Array(String(describing: v).utf8)
        return "OPAQUE:" + _hx(u)
    }
}
func _emit<T>(_ id: String, _ v: T) {
    print("\(id)|\(T.self)|\(_enc(v))")
}
'''

RT_DART = r'''
import 'dart:io';
import 'dart:convert';
import 'dart:typed_data';

String _hx(List<int> b) =>
    b.map((x) => x.toRadixString(16).padLeft(2, '0')).join();

String _enc(dynamic v) {
  if (v == null) return 'NULL';
  if (v is bool) return 'BOOL:$v';
  if (v is int) {
    final bd = ByteData(8);
    bd.setInt64(0, v);
    return 'INT:64:' + _hx(bd.buffer.asUint8List());
  }
  if (v is double) {
    final bd = ByteData(8);
    bd.setFloat64(0, v);
    return 'FLOAT:64:' + _hx(bd.buffer.asUint8List());
  }
  if (v is BigInt) {
    return 'BIGINT:' + (v.isNegative ? '-' : '') + v.abs().toRadixString(16);
  }
  if (v is String) {
    final u = utf8.encode(v);
    return 'STR:${v.length}:${u.length}:' + _hx(u);
  }
  if (v is Map) {
    final ps = <String>[];
    v.forEach((k, x) => ps.add(_enc(k) + '=>' + _enc(x)));
    ps.sort();
    return 'MAP:${ps.length}[' + ps.join(',') + ']';
  }
  if (v is Set) {
    final ps = v.map((e) => _enc(e)).toList();
    ps.sort();
    return 'LIST:${ps.length}[' + ps.join(',') + ']';
  }
  if (v is Iterable) {
    final ps = v.map((e) => _enc(e)).toList();
    return 'LIST:${ps.length}[' + ps.join(',') + ']';
  }
  return 'OPAQUE:' + _hx(utf8.encode(v.toString()));
}

void _emit<T>(String id, T v) {
  stdout.writeln('$id|$T|' + _enc(v));
}
'''

RT_CSHARP = r'''
using System;
using System.Text;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;

static class RT {
  static string Hx(byte[] b) {
    var sb = new StringBuilder();
    foreach (var x in b) sb.Append(x.ToString("x2"));
    return sb.ToString();
  }
  static string Be(byte[] b) {
    if (BitConverter.IsLittleEndian) Array.Reverse(b);
    return Hx(b);
  }
  public static string Enc(object v) {
    if (v == null) return "NULL";
    switch (v) {
      case bool x: return "BOOL:" + (x ? "true" : "false");
      case sbyte x: return "INT:8:" + Be(new byte[]{ (byte)x });
      case byte x: return "UINT:8:" + Be(new byte[]{ x });
      case short x: return "INT:16:" + Be(BitConverter.GetBytes(x));
      case ushort x: return "UINT:16:" + Be(BitConverter.GetBytes(x));
      case int x: return "INT:32:" + Be(BitConverter.GetBytes(x));
      case uint x: return "UINT:32:" + Be(BitConverter.GetBytes(x));
      case long x: return "INT:64:" + Be(BitConverter.GetBytes(x));
      case ulong x: return "UINT:64:" + Be(BitConverter.GetBytes(x));
      case nint x: return "INT:64:" + Be(BitConverter.GetBytes((long)x));
      case nuint x: return "UINT:64:" + Be(BitConverter.GetBytes((ulong)x));
      case float x: return "FLOAT:32:" + Be(BitConverter.GetBytes(x));
      case double x: return "FLOAT:64:" + Be(BitConverter.GetBytes(x));
      case decimal x: {
        var bits = decimal.GetBits(x);
        var sb = new StringBuilder("DEC128:");
        foreach (var w in bits) sb.Append(Be(BitConverter.GetBytes(w)));
        return sb.ToString();
      }
      case char x: return "CHAR:" + ((int)x).ToString("x4");
      case string x: {
        var u = Encoding.UTF8.GetBytes(x);
        return "STR:" + x.Length + ":" + u.Length + ":" + Hx(u);
      }
      case IDictionary d: {
        var ps = new List<string>();
        foreach (DictionaryEntry e in d) ps.Add(Enc(e.Key) + "=>" + Enc(e.Value));
        ps.Sort(StringComparer.Ordinal);
        return "MAP:" + ps.Count + "[" + string.Join(",", ps) + "]";
      }
      case IEnumerable s: {
        var ps = new List<string>();
        foreach (var e in s) ps.Add(Enc(e));
        return "LIST:" + ps.Count + "[" + string.Join(",", ps) + "]";
      }
    }
    return "OPAQUE:" + Hx(Encoding.UTF8.GetBytes(
        Convert.ToString(v, CultureInfo.InvariantCulture) ?? ""));
  }
  public static void Emit<T>(string id, T v) {
    Console.Out.Write(id + "|" + typeof(T).ToString() + "|" + Enc(v) + "\n");
    Console.Out.Flush();
  }
  public static void Raise(string id, string what) {
    Console.Out.Write(id + "|-|RAISE:" + what + "\n");
    Console.Out.Flush();
  }
}
'''

RT_JAVA = r'''
import java.util.*;
import java.nio.charset.StandardCharsets;
import java.lang.reflect.Array;

class RT {
  static final StringBuilder SB = new StringBuilder();
  static String hx(byte[] b) {
    StringBuilder s = new StringBuilder();
    for (byte x : b) s.append(String.format("%02x", x));
    return s.toString();
  }
  static String ih(long v, int bits) {
    String s = Long.toHexString(v);
    int n = bits / 4;
    while (s.length() < n) s = "0" + s;
    if (s.length() > n) s = s.substring(s.length() - n);
    return s;
  }
  static String enc(Object v) {
    if (v == null) return "NULL";
    if (v instanceof Boolean) return "BOOL:" + v;
    if (v instanceof Byte) return "INT:8:" + ih((Byte) v, 8);
    if (v instanceof Short) return "INT:16:" + ih((Short) v, 16);
    if (v instanceof Integer) return "INT:32:" + ih((Integer) v, 32);
    if (v instanceof Long) return "INT:64:" + ih((Long) v, 64);
    if (v instanceof Character)
      return "CHAR:" + ih((long) (char) (Character) v, 16);
    if (v instanceof Float)
      return "FLOAT:32:" + ih(Float.floatToRawIntBits((Float) v) & 0xffffffffL, 32);
    if (v instanceof Double)
      return "FLOAT:64:" + ih(Double.doubleToRawLongBits((Double) v), 64);
    if (v instanceof java.math.BigInteger)
      return "BIGINT:" + hx(((java.math.BigInteger) v).toByteArray());
    if (v instanceof String) {
      String s = (String) v;
      byte[] u = s.getBytes(StandardCharsets.UTF_8);
      return "STR:" + s.length() + ":" + u.length + ":" + hx(u);
    }
    if (v instanceof Map) {
      List<String> ps = new ArrayList<>();
      for (Object o : ((Map<?, ?>) v).entrySet()) {
        Map.Entry<?, ?> e = (Map.Entry<?, ?>) o;
        ps.add(enc(e.getKey()) + "=>" + enc(e.getValue()));
      }
      Collections.sort(ps);
      return "MAP:" + ps.size() + "[" + String.join(",", ps) + "]";
    }
    if (v instanceof Iterable) {
      List<String> ps = new ArrayList<>();
      for (Object o : (Iterable<?>) v) ps.add(enc(o));
      return "LIST:" + ps.size() + "[" + String.join(",", ps) + "]";
    }
    if (v.getClass().isArray()) {
      int n = Array.getLength(v);
      List<String> ps = new ArrayList<>();
      for (int i = 0; i < n; i++) ps.add(enc(Array.get(v, i)));
      return "LIST:" + n + "[" + String.join(",", ps) + "]";
    }
    return "OPAQUE:" + hx(String.valueOf(v).getBytes(StandardCharsets.UTF_8));
  }
  static void w(String id, String tn, String body) {
    System.out.println(id + "|" + tn + "|" + body);
    System.out.flush();
  }
  static void emit(String id, boolean v) { w(id, "boolean", enc(v)); }
  static void emit(String id, byte v) { w(id, "byte", enc(v)); }
  static void emit(String id, short v) { w(id, "short", enc(v)); }
  static void emit(String id, char v) { w(id, "char", enc(v)); }
  static void emit(String id, int v) { w(id, "int", enc(v)); }
  static void emit(String id, long v) { w(id, "long", enc(v)); }
  static void emit(String id, float v) { w(id, "float", enc(v)); }
  static void emit(String id, double v) { w(id, "double", enc(v)); }
  static void emit(String id, Object v) {
    w(id, v == null ? "null" : v.getClass().getName(), enc(v));
  }
  static void raise(String id, Throwable t) {
    System.out.println(id + "|-|RAISE:" + t.getClass().getName());
    System.out.flush();
  }
}
'''

RT_KOTLIN = r'''
object RT {
  fun hx(b: ByteArray): String {
    val s = StringBuilder()
    for (x in b) s.append(String.format("%02x", x))
    return s.toString()
  }
  fun ih(v: Long, bits: Int): String {
    var s = java.lang.Long.toHexString(v)
    val n = bits / 4
    while (s.length < n) s = "0" + s
    if (s.length > n) s = s.substring(s.length - n)
    return s
  }
  fun enc(v: Any?): String {
    if (v == null) return "NULL"
    when (v) {
      is Boolean -> return "BOOL:" + v
      is Byte -> return "INT:8:" + ih(v.toLong(), 8)
      is Short -> return "INT:16:" + ih(v.toLong(), 16)
      is Int -> return "INT:32:" + ih(v.toLong(), 32)
      is Long -> return "INT:64:" + ih(v, 64)
      is Char -> return "CHAR:" + ih(v.code.toLong(), 16)
      is Float -> return "FLOAT:32:" +
          ih(java.lang.Float.floatToRawIntBits(v).toLong() and 0xffffffffL, 32)
      is Double -> return "FLOAT:64:" +
          ih(java.lang.Double.doubleToRawLongBits(v), 64)
      is java.math.BigInteger -> return "BIGINT:" + hx(v.toByteArray())
      is String -> {
        val u = v.toByteArray(Charsets.UTF_8)
        return "STR:" + v.length + ":" + u.size + ":" + hx(u)
      }
      // RANGES BEFORE ITERABLES, and it matters: kotlin's `..` returns a
      // LongRange, a LongRange IS an Iterable, and `0..Long.MAX_VALUE`
      // walked as an iterable does not come back.  Measured 2026-08-19.
      is IntRange -> return "RANGE[" + enc(v.first) + "," + enc(v.last) + ",incl]"
      is LongRange -> return "RANGE[" + enc(v.first) + "," + enc(v.last) + ",incl]"
      is CharRange -> return "RANGE[" + enc(v.first) + "," + enc(v.last) + ",incl]"
      is Map<*, *> -> {
        val ps = ArrayList<String>()
        for (e in v.entries) ps.add(enc(e.key) + "=>" + enc(e.value))
        ps.sort()
        return "MAP:" + ps.size + "[" + ps.joinToString(",") + "]"
      }
      is Iterable<*> -> {
        val ps = ArrayList<String>()
        var n = 0
        for (e in v) {
          if (n >= 1000) { ps.add("TRUNC"); break }
          ps.add(enc(e)); n++
        }
        return "LIST:" + ps.size + "[" + ps.joinToString(",") + "]"
      }
    }
    // JAVA ARRAYS.  kotlin's `?:` and `in` hand back `CharArray` and
    // friends, whose `toString` is `[C@4b1210ee` -- an identity hash,
    // which differs between two runs of the same probe.  A recorder that
    // writes one is recording the heap, not the answer.  Measured
    // 2026-08-19 by diffing two kotlin runs: 2,645 rows moved and every
    // one was of this shape.
    if (v.javaClass.isArray) {
      val n = java.lang.reflect.Array.getLength(v)
      val ps = ArrayList<String>()
      var i = 0
      while (i < n && i < 1000) {
        ps.add(enc(java.lang.reflect.Array.get(v, i))); i++
      }
      if (n > 1000) ps.add("TRUNC")
      return "LIST:" + n + "[" + ps.joinToString(",") + "]"
    }
    return "OPAQUE:" + hx(v.toString().toByteArray(Charsets.UTF_8))
  }
  fun w(id: String, tn: String, body: String) {
    println(id + "|" + tn + "|" + body)
    System.out.flush()
  }
  fun emit(id: String, v: Boolean) { w(id, "kotlin.Boolean", enc(v)) }
  fun emit(id: String, v: Byte) { w(id, "kotlin.Byte", enc(v)) }
  fun emit(id: String, v: Short) { w(id, "kotlin.Short", enc(v)) }
  fun emit(id: String, v: Char) { w(id, "kotlin.Char", enc(v)) }
  fun emit(id: String, v: Int) { w(id, "kotlin.Int", enc(v)) }
  fun emit(id: String, v: Long) { w(id, "kotlin.Long", enc(v)) }
  fun emit(id: String, v: Float) { w(id, "kotlin.Float", enc(v)) }
  fun emit(id: String, v: Double) { w(id, "kotlin.Double", enc(v)) }
  fun emit(id: String, v: Any?) {
    w(id, if (v == null) "null" else v.javaClass.name, enc(v))
  }
  fun raise(id: String, t: Throwable) {
    println(id + "|-|RAISE:" + t.javaClass.name)
    System.out.flush()
  }
}
'''

RT_TS = r'''
function _hx(b: any): string {
  let s = "";
  for (let i = 0; i < b.length; i++) s += b[i].toString(16).padStart(2, "0");
  return s;
}
function _utf8(s: string): number[] {
  const out: number[] = [];
  for (const ch of s) {
    let c = ch.codePointAt(0) as number;
    if (c < 0x80) out.push(c);
    else if (c < 0x800) out.push(0xc0 | (c >> 6), 0x80 | (c & 63));
    else if (c < 0x10000)
      out.push(0xe0 | (c >> 12), 0x80 | ((c >> 6) & 63), 0x80 | (c & 63));
    else
      out.push(0xf0 | (c >> 18), 0x80 | ((c >> 12) & 63),
               0x80 | ((c >> 6) & 63), 0x80 | (c & 63));
  }
  return out;
}
function _enc(v: any): string {
  if (v === null) return "NULL";
  if (v === undefined) return "UNDEFINED";
  const t = typeof v;
  if (t === "boolean") return "BOOL:" + v;
  if (t === "number") {
    const b = new Uint8Array(8);
    new DataView(b.buffer).setFloat64(0, v, false);
    return "FLOAT:64:" + _hx(b);
  }
  if (t === "bigint") {
    let n: bigint = v as bigint;
    const neg = n < 0n;
    let h = (neg ? -n : n).toString(16);
    return "BIGINT:" + (neg ? "-" : "") + h;
  }
  if (t === "string") {
    const u = _utf8(v);
    return "STR:" + v.length + ":" + u.length + ":" + _hx(u);
  }
  if (t === "symbol" || t === "function")
    return "OPAQUE:" + _hx(_utf8(String(v)));
  if (Array.isArray(v))
    return "LIST:" + v.length + "[" + v.map(_enc).join(",") + "]";
  if (v instanceof Map) {
    const ps: string[] = [];
    v.forEach((x: any, k: any) => ps.push(_enc(k) + "=>" + _enc(x)));
    ps.sort();
    return "MAP:" + ps.length + "[" + ps.join(",") + "]";
  }
  if (v instanceof Set) {
    const ps: string[] = [];
    v.forEach((x: any) => ps.push(_enc(x)));
    ps.sort();
    return "LIST:" + ps.length + "[" + ps.join(",") + "]";
  }
  try {
    const ks = Object.keys(v).sort();
    const ps = ks.map((k) => _enc(k) + "=>" + _enc((v as any)[k]));
    return "STRUCT:" + ps.length + "[" + ps.join(",") + "]";
  } catch (e) {
    return "OPAQUE:";
  }
}
function _tn(v: any): string {
  if (v === null) return "null";
  const t = typeof v;
  if (t !== "object") return t;
  try {
    return (v.constructor && v.constructor.name) || "Object";
  } catch (e) {
    return "object";
  }
}
function _emit(id: string, v: any): void {
  process.stdout.write(id + "|" + _tn(v) + "|" + _enc(v) + "\n");
}
'''

RT = dict(go=RT_GO, rust=RT_RUST, cpp=RT_CPP, swift=RT_SWIFT, dart=RT_DART,
          csharp=RT_CSHARP, java=RT_JAVA, kotlin=RT_KOTLIN, typescript=RT_TS)


def main():
    which = sys.argv[1:] or LANGS
    plan = {}
    for lang in which:
        ids = accepted(lang)
        ch = CHUNK[lang]
        shards = [ids[i:i + ch] for i in range(0, len(ids), ch)]
        plan[lang] = dict(probes=len(ids), chunk=ch, chunks=len(shards),
                          catchable=CATCHABLE[lang])
        print("== %-11s %7d accepted probes, %4d per chunk, %3d chunks"
              % (lang, len(ids), ch, len(shards)))
    json.dump(plan, open(os.path.join(HERE, "exec_plan.json"), "w"), indent=1)
    print("\n| language | accepted probes | chunk | chunks | catchable |")
    print("|---|---|---|---|---|")
    for lang in which:
        p = plan[lang]
        print("| %s | %d | %d | %d | %s |"
              % (lang, p["probes"], p["chunk"], p["chunks"], p["catchable"]))
    print("\ntotal accepted probes: %d"
          % sum(p["probes"] for p in plan.values()))


if __name__ == "__main__":
    main()
