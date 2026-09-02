
using System;
using System.Collections.Generic;
using System.Numerics;

public static class BND {
  static readonly HashSet<string> EXACT = new HashSet<string>(
      new string[] {"+", "-", "*", "<", "<=", ">", ">=", "==", "!="});

  static object wantv(string op, BigInteger a, BigInteger b) {
    if (!EXACT.Contains(op)) return null;
    switch (op) {
      case "+": return a + b;
      case "-": return a - b;
      case "*": return a * b;
      case "<": return a < b;
      case "<=": return a <= b;
      case ">": return a > b;
      case ">=": return a >= b;
      case "==": return a == b;
      case "!=": return a != b;
    }
    return null;
  }

  static object asint(object r) {
    if (r is bool) return r;
    if (r is BigInteger) return r;
    if (r is short || r is int || r is long)
      return new BigInteger(Convert.ToInt64(r));
    if (r is ushort || r is uint || r is ulong)
      return new BigInteger(Convert.ToUInt64(r));
    if (r is double || r is float) {
      double d = Convert.ToDouble(r);
      if (double.IsNaN(d) || double.IsInfinity(d)) return null;
      if (d != Math.Floor(d)) return "NONINT";
      return new BigInteger(d);
    }
    if (r is decimal) {
      decimal m = (decimal) r;
      if (m != Math.Floor(m)) return "NONINT";
      return new BigInteger(m);
    }
    return null;
  }

  static string fidv(object r, string op, BigInteger a, BigInteger b) {
    object w = wantv(op, a, b);
    if (w == null) return "na";
    object g = asint(r);
    if (g == null) return "na";
    if (w is bool) {
      if (!(g is bool)) return "na";
      return ((bool) w) == ((bool) g) ? "exact" : "inexact";
    }
    if (g is bool) return "na";
    if ((g as string) == "NONINT") return "inexact";
    return ((BigInteger) g) == ((BigInteger) w) ? "exact" : "inexact";
  }

  static string sigv(Func<BigInteger, object> fn, BigInteger c, string op,
                     BigInteger a, BigInteger b) {
    object r;
    try { r = fn(c); }
    catch (Exception e) { return "raise|" + e.GetType().Name + "|na"; }
    string tn = (r == null) ? "null" : r.GetType().Name;
    return "answer|" + tn + "|" + fidv(r, op, a, b);
  }

  public static int bisect(int tid, Func<BigInteger, object> fn, string op,
                           BigInteger lov, BigInteger hiv, BigInteger fixedv,
                           bool varyIsLhs) {
    Func<BigInteger, string> s = (c) => {
      BigInteger a = varyIsLhs ? c : fixedv;
      BigInteger b = varyIsLhs ? fixedv : c;
      return sigv(fn, c, op, a, b);
    };
    BigInteger lo = lov, hi = hiv;
    string slo = s(lo), shi = s(hi);
    int probes = 2;
    if (slo == shi) { Console.WriteLine("N|" + tid + "|" + slo + "|" + shi); return probes; }
    SortedSet<string> other = new SortedSet<string>();
    while (hi - lo > 1) {
      BigInteger mid = (lo + hi) / 2;
      string sm = s(mid); probes++;
      if (sm == slo) lo = mid;
      else { if (sm != shi) other.Add(sm); hi = mid; }
    }
    Console.WriteLine("B|" + tid + "|" + lo + "|" + hi + "|" + slo + "|" +
                      shi + "|" + probes + "|" + string.Join(";", other));
    return probes;
  }

  static readonly List<Func<int>> TARGETS = new List<Func<int>>();
  static void Reg() {
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(1954, (c) => ((object)(((int)(long)(c)) + (f))), "+", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), true); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(1955, (c) => ((object)(((int)(long)(c)) * (f))), "*", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), true); });
    TARGETS.Add(() => { int f = 42; return bisect(1964, (c) => ((object)(((long)(c)) + (f))), "+", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), true); });
    TARGETS.Add(() => { int f = 42; return bisect(1965, (c) => ((object)(((long)(c)) * (f))), "*", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), true); });
    TARGETS.Add(() => { long f = 42L; return bisect(1966, (c) => ((object)(((long)(c)) + (f))), "+", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), true); });
    TARGETS.Add(() => { long f = 42L; return bisect(1967, (c) => ((object)(((long)(c)) * (f))), "*", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), true); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(1968, (c) => ((object)(((long)(c)) + (f))), "+", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), true); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(1969, (c) => ((object)(((long)(c)) * (f))), "*", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), true); });
    TARGETS.Add(() => { long f = 9007199254740993L; return bisect(1970, (c) => ((object)(((long)(c)) + (f))), "+", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("9007199254740993"), true); });
    TARGETS.Add(() => { long f = 9007199254740993L; return bisect(1971, (c) => ((object)(((long)(c)) * (f))), "*", BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), BigInteger.Parse("9007199254740993"), true); });
    TARGETS.Add(() => { short f = (short)42; return bisect(1972, (c) => ((object)(((long)(c)) + (f))), "+", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), true); });
    TARGETS.Add(() => { short f = (short)42; return bisect(1973, (c) => ((object)(((long)(c)) * (f))), "*", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), true); });
    TARGETS.Add(() => { ulong f = 42UL; return bisect(1992, (c) => ((object)(((ulong)(c)) + (f))), "+", BigInteger.Parse("9223372036854775808"), BigInteger.Parse("18446744073709551615"), BigInteger.Parse("42"), true); });
    TARGETS.Add(() => { ulong f = 42UL; return bisect(1993, (c) => ((object)(((ulong)(c)) - (f))), "-", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), true); });
    TARGETS.Add(() => { ulong f = 42UL; return bisect(1994, (c) => ((object)(((ulong)(c)) * (f))), "*", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), true); });
    TARGETS.Add(() => { ulong f = 9223372036854775807UL; return bisect(1995, (c) => ((object)(((ulong)(c)) + (f))), "+", BigInteger.Parse("9223372036854775808"), BigInteger.Parse("18446744073709551615"), BigInteger.Parse("9223372036854775807"), true); });
    TARGETS.Add(() => { ulong f = 9223372036854775807UL; return bisect(1996, (c) => ((object)(((ulong)(c)) - (f))), "-", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("9223372036854775807"), true); });
    TARGETS.Add(() => { ulong f = 9223372036854775807UL; return bisect(1997, (c) => ((object)(((ulong)(c)) * (f))), "*", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), true); });
    TARGETS.Add(() => { ulong f = 9223372036854775808UL; return bisect(1998, (c) => ((object)(((ulong)(c)) * (f))), "*", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), true); });
    TARGETS.Add(() => { ulong f = 9007199254740993UL; return bisect(1999, (c) => ((object)(((ulong)(c)) + (f))), "+", BigInteger.Parse("9223372036854775808"), BigInteger.Parse("18446744073709551615"), BigInteger.Parse("9007199254740993"), true); });
    TARGETS.Add(() => { ulong f = 9007199254740993UL; return bisect(2000, (c) => ((object)(((ulong)(c)) - (f))), "-", BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), BigInteger.Parse("9007199254740993"), true); });
    TARGETS.Add(() => { ulong f = 9007199254740993UL; return bisect(2001, (c) => ((object)(((ulong)(c)) * (f))), "*", BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), BigInteger.Parse("9007199254740993"), true); });
    TARGETS.Add(() => { ulong f = 18446744073709551615UL; return bisect(2002, (c) => ((object)(((ulong)(c)) + (f))), "+", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), true); });
    TARGETS.Add(() => { ulong f = 18446744073709551615UL; return bisect(2003, (c) => ((object)(((ulong)(c)) - (f))), "-", BigInteger.Parse("9223372036854775808"), BigInteger.Parse("18446744073709551615"), BigInteger.Parse("18446744073709551615"), true); });
    TARGETS.Add(() => { ulong f = 18446744073709551615UL; return bisect(2004, (c) => ((object)(((ulong)(c)) * (f))), "*", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), true); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2031, (c) => ((object)(((short)(long)(c)) + (f))), "+", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), true); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2032, (c) => ((object)(((short)(long)(c)) * (f))), "*", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), true); });
    TARGETS.Add(() => { int f = 42; return bisect(2041, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { int f = 42; return bisect(2042, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { int f = 0; return bisect(2043, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { int f = 0; return bisect(2044, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { int f = 42; return bisect(2045, (c) => ((object)((f) + ((long)(c)))), "+", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { int f = 42; return bisect(2046, (c) => ((object)((f) * ((long)(c)))), "*", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { int f = 42; return bisect(2047, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { int f = 42; return bisect(2048, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { int f = 0; return bisect(2049, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { int f = 0; return bisect(2050, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { int f = 42; return bisect(2051, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { int f = 42; return bisect(2052, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { int f = 0; return bisect(2053, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { int f = 0; return bisect(2054, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { int f = 42; return bisect(2055, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { int f = 42; return bisect(2056, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { int f = 0; return bisect(2057, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { int f = 0; return bisect(2058, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { long f = 42L; return bisect(2059, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { long f = 42L; return bisect(2060, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { long f = 0L; return bisect(2061, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { long f = 0L; return bisect(2062, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2063, (c) => ((object)((f) + ((int)(long)(c)))), "+", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2064, (c) => ((object)((f) * ((int)(long)(c)))), "*", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2065, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2066, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9007199254740993L; return bisect(2067, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { long f = 9007199254740993L; return bisect(2068, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { long f = 42L; return bisect(2069, (c) => ((object)((f) + ((long)(c)))), "+", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { long f = 42L; return bisect(2070, (c) => ((object)((f) * ((long)(c)))), "*", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { long f = 42L; return bisect(2071, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { long f = 42L; return bisect(2072, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { long f = 0L; return bisect(2073, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { long f = 0L; return bisect(2074, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2075, (c) => ((object)((f) + ((long)(c)))), "+", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2076, (c) => ((object)((f) * ((long)(c)))), "*", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2077, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2078, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9007199254740993L; return bisect(2079, (c) => ((object)((f) + ((long)(c)))), "+", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { long f = 9007199254740993L; return bisect(2080, (c) => ((object)((f) * ((long)(c)))), "*", BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { long f = 9007199254740993L; return bisect(2081, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { long f = 9007199254740993L; return bisect(2082, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { long f = 42L; return bisect(2083, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { long f = 42L; return bisect(2084, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { long f = 0L; return bisect(2085, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { long f = 0L; return bisect(2086, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2087, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2088, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9007199254740993L; return bisect(2089, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { long f = 9007199254740993L; return bisect(2090, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { long f = 42L; return bisect(2091, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { long f = 42L; return bisect(2092, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { long f = 0L; return bisect(2093, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { long f = 0L; return bisect(2094, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2095, (c) => ((object)((f) + ((short)(long)(c)))), "+", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2096, (c) => ((object)((f) * ((short)(long)(c)))), "*", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2097, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9223372036854775807L; return bisect(2098, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { long f = 9007199254740993L; return bisect(2099, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { long f = 9007199254740993L; return bisect(2100, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { ulong f = 42UL; return bisect(2101, (c) => ((object)((f) + ((ulong)(c)))), "+", BigInteger.Parse("9223372036854775808"), BigInteger.Parse("18446744073709551615"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { ulong f = 42UL; return bisect(2102, (c) => ((object)((f) - ((ulong)(c)))), "-", BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { ulong f = 42UL; return bisect(2103, (c) => ((object)((f) * ((ulong)(c)))), "*", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { ulong f = 42UL; return bisect(2104, (c) => ((object)((f) / ((ulong)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { ulong f = 42UL; return bisect(2105, (c) => ((object)((f) % ((ulong)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { ulong f = 0UL; return bisect(2106, (c) => ((object)((f) - ((ulong)(c)))), "-", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { ulong f = 0UL; return bisect(2107, (c) => ((object)((f) / ((ulong)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { ulong f = 0UL; return bisect(2108, (c) => ((object)((f) % ((ulong)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { ulong f = 9223372036854775807UL; return bisect(2109, (c) => ((object)((f) + ((ulong)(c)))), "+", BigInteger.Parse("9223372036854775808"), BigInteger.Parse("18446744073709551615"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { ulong f = 9223372036854775807UL; return bisect(2110, (c) => ((object)((f) * ((ulong)(c)))), "*", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { ulong f = 9223372036854775807UL; return bisect(2111, (c) => ((object)((f) / ((ulong)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { ulong f = 9223372036854775807UL; return bisect(2112, (c) => ((object)((f) % ((ulong)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { ulong f = 9223372036854775808UL; return bisect(2113, (c) => ((object)((f) - ((ulong)(c)))), "-", BigInteger.Parse("9223372036854775808"), BigInteger.Parse("18446744073709551615"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { ulong f = 9223372036854775808UL; return bisect(2114, (c) => ((object)((f) * ((ulong)(c)))), "*", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { ulong f = 9223372036854775808UL; return bisect(2115, (c) => ((object)((f) / ((ulong)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { ulong f = 9223372036854775808UL; return bisect(2116, (c) => ((object)((f) % ((ulong)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { ulong f = 9007199254740993UL; return bisect(2117, (c) => ((object)((f) + ((ulong)(c)))), "+", BigInteger.Parse("9223372036854775808"), BigInteger.Parse("18446744073709551615"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { ulong f = 9007199254740993UL; return bisect(2118, (c) => ((object)((f) - ((ulong)(c)))), "-", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { ulong f = 9007199254740993UL; return bisect(2119, (c) => ((object)((f) * ((ulong)(c)))), "*", BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { ulong f = 9007199254740993UL; return bisect(2120, (c) => ((object)((f) / ((ulong)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { ulong f = 9007199254740993UL; return bisect(2121, (c) => ((object)((f) % ((ulong)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { ulong f = 18446744073709551615UL; return bisect(2122, (c) => ((object)((f) + ((ulong)(c)))), "+", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { ulong f = 18446744073709551615UL; return bisect(2123, (c) => ((object)((f) * ((ulong)(c)))), "*", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { ulong f = 18446744073709551615UL; return bisect(2124, (c) => ((object)((f) / ((ulong)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { ulong f = 18446744073709551615UL; return bisect(2125, (c) => ((object)((f) % ((ulong)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { ulong f = 42UL; return bisect(2126, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { ulong f = 42UL; return bisect(2127, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { ulong f = 0UL; return bisect(2128, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { ulong f = 0UL; return bisect(2129, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { ulong f = 9223372036854775807UL; return bisect(2130, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { ulong f = 9223372036854775807UL; return bisect(2131, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { ulong f = 9223372036854775808UL; return bisect(2132, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { ulong f = 9223372036854775808UL; return bisect(2133, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { ulong f = 9007199254740993UL; return bisect(2134, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { ulong f = 9007199254740993UL; return bisect(2135, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { ulong f = 18446744073709551615UL; return bisect(2136, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { ulong f = 18446744073709551615UL; return bisect(2137, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("42"); return bisect(2138, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("42"); return bisect(2139, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("0"); return bisect(2140, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("0"); return bisect(2141, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775807"); return bisect(2142, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775807"); return bisect(2143, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775808"); return bisect(2144, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775808"); return bisect(2145, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9007199254740993"); return bisect(2146, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9007199254740993"); return bisect(2147, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("18446744073709551615"); return bisect(2148, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("18446744073709551615"); return bisect(2149, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("42"); return bisect(2150, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("42"); return bisect(2151, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("0"); return bisect(2152, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("0"); return bisect(2153, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775807"); return bisect(2154, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775807"); return bisect(2155, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775808"); return bisect(2156, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775808"); return bisect(2157, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9007199254740993"); return bisect(2158, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9007199254740993"); return bisect(2159, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("18446744073709551615"); return bisect(2160, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("18446744073709551615"); return bisect(2161, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("42"); return bisect(2162, (c) => ((object)((f) / ((ulong)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("42"); return bisect(2163, (c) => ((object)((f) % ((ulong)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("0"); return bisect(2164, (c) => ((object)((f) / ((ulong)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("0"); return bisect(2165, (c) => ((object)((f) % ((ulong)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775807"); return bisect(2166, (c) => ((object)((f) / ((ulong)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775807"); return bisect(2167, (c) => ((object)((f) % ((ulong)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775808"); return bisect(2168, (c) => ((object)((f) / ((ulong)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775808"); return bisect(2169, (c) => ((object)((f) % ((ulong)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9007199254740993"); return bisect(2170, (c) => ((object)((f) / ((ulong)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9007199254740993"); return bisect(2171, (c) => ((object)((f) % ((ulong)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("18446744073709551615"); return bisect(2172, (c) => ((object)((f) / ((ulong)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("18446744073709551615"); return bisect(2173, (c) => ((object)((f) % ((ulong)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("42"); return bisect(2174, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("42"); return bisect(2175, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("0"); return bisect(2176, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("0"); return bisect(2177, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775807"); return bisect(2178, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775807"); return bisect(2179, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775808"); return bisect(2180, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775808"); return bisect(2181, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9007199254740993"); return bisect(2182, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9007199254740993"); return bisect(2183, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("18446744073709551615"); return bisect(2184, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("18446744073709551615"); return bisect(2185, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("42"); return bisect(2186, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("42"); return bisect(2187, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("0"); return bisect(2188, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("0"); return bisect(2189, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775807"); return bisect(2190, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775807"); return bisect(2191, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775807"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775808"); return bisect(2192, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9223372036854775808"); return bisect(2193, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9223372036854775808"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9007199254740993"); return bisect(2194, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("9007199254740993"); return bisect(2195, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("9007199254740993"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("18446744073709551615"); return bisect(2196, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { BigInteger f = BigInteger.Parse("18446744073709551615"); return bisect(2197, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("18446744073709551615"), false); });
    TARGETS.Add(() => { short f = (short)42; return bisect(2198, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { short f = (short)42; return bisect(2199, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { short f = (short)0; return bisect(2200, (c) => ((object)((f) / ((int)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { short f = (short)0; return bisect(2201, (c) => ((object)((f) % ((int)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { short f = (short)42; return bisect(2202, (c) => ((object)((f) + ((long)(c)))), "+", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { short f = (short)42; return bisect(2203, (c) => ((object)((f) * ((long)(c)))), "*", BigInteger.Parse("9007199254740993"), BigInteger.Parse("9223372036854775807"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { short f = (short)42; return bisect(2204, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { short f = (short)42; return bisect(2205, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { short f = (short)0; return bisect(2206, (c) => ((object)((f) / ((long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { short f = (short)0; return bisect(2207, (c) => ((object)((f) % ((long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { short f = (short)42; return bisect(2208, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { short f = (short)42; return bisect(2209, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { short f = (short)0; return bisect(2210, (c) => ((object)((f) / ((c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { short f = (short)0; return bisect(2211, (c) => ((object)((f) % ((c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { short f = (short)42; return bisect(2212, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { short f = (short)42; return bisect(2213, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("42"), false); });
    TARGETS.Add(() => { short f = (short)0; return bisect(2214, (c) => ((object)((f) / ((short)(long)(c)))), "/", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
    TARGETS.Add(() => { short f = (short)0; return bisect(2215, (c) => ((object)((f) % ((short)(long)(c)))), "%", BigInteger.Parse("0"), BigInteger.Parse("42"), BigInteger.Parse("0"), false); });
  }

  public static void Main() {
    Reg();
    int total = 0;
    int n = TARGETS.Count;
    for (int k = 0; k < n; k++) {
      total += TARGETS[k]();
      if ((k + 1) % 25 == 0 || k + 1 == n)
        Console.Error.WriteLine("progress " + (k + 1) + "/" + n +
                                " probes=" + total);
    }
    Console.Error.WriteLine("DONE targets=" + n + " probes=" + total);
  }
}
