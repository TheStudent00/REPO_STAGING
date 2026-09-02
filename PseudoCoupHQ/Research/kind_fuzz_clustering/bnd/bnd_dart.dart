
import 'dart:io';

const EXACT = ["+", "-", "*", "<", "<=", ">", ">=", "==", "!="];

dynamic wantv(String op, BigInt a, BigInt b) {
  if (!EXACT.contains(op)) return null;
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

dynamic asint(dynamic r) {
  if (r is bool) return r;
  if (r is BigInt) return r;
  if (r is int) return BigInt.from(r);
  if (r is double) {
    if (r.isNaN || r.isInfinite) return null;
    if (r != r.truncateToDouble()) return "NONINT";
    return BigInt.from(r);
  }
  return null;
}

String fidv(dynamic r, String op, BigInt a, BigInt b) {
  var w = wantv(op, a, b);
  if (w == null) return "na";
  var g = asint(r);
  if (g == null) return "na";
  if (w is bool) {
    if (g is! bool) return "na";
    return w == g ? "exact" : "inexact";
  }
  if (g is bool) return "na";
  if (g == "NONINT") return "inexact";
  return (g as BigInt) == (w as BigInt) ? "exact" : "inexact";
}

String sigv(dynamic Function(BigInt) fn, BigInt c, String op,
            BigInt a, BigInt b) {
  dynamic r;
  try { r = fn(c); }
  catch (e) { return "raise|" + e.runtimeType.toString() + "|na"; }
  return "answer|" + r.runtimeType.toString() + "|" + fidv(r, op, a, b);
}

int bisect(int tid, dynamic Function(BigInt) fn, String op,
           BigInt lov, BigInt hiv, BigInt fixed, bool varyIsLhs) {
  String s(BigInt c) {
    var a = varyIsLhs ? c : fixed;
    var b = varyIsLhs ? fixed : c;
    return sigv(fn, c, op, a, b);
  }
  var lo = lov, hi = hiv;
  var slo = s(lo), shi = s(hi);
  var probes = 2;
  if (slo == shi) { print("N|$tid|$slo|$shi"); return probes; }
  var other = <String>{};
  while (hi - lo > BigInt.one) {
    var mid = (lo + hi) ~/ BigInt.two;
    var sm = s(mid); probes++;
    if (sm == slo) { lo = mid; }
    else { if (sm != shi) other.add(sm); hi = mid; }
  }
  var o = other.toList()..sort();
  print("B|$tid|$lo|$hi|$slo|$shi|$probes|${o.join(';')}");
  return probes;
}

final TARGETS = <int Function()>[
  () { int f = 42; return bisect(1732, (BigInt c) => (((c).toInt()) * (f)), "*", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("42"), true); },
  () { int f = 9223372036854775807; return bisect(1733, (BigInt c) => (((c).toInt()) * (f)), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), true); },
  () { int f = 9007199254740993; return bisect(1734, (BigInt c) => (((c).toInt()) * (f)), "*", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9007199254740993"), true); },
  () { BigInt f = BigInt.parse("42"); return bisect(1735, (BigInt c) => (((c).toInt()) == (f)), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), true); },
  () { BigInt f = BigInt.parse("42"); return bisect(1736, (BigInt c) => (((c).toInt()) == (f)), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), true); },
  () { BigInt f = BigInt.parse("0"); return bisect(1737, (BigInt c) => (((c).toInt()) == (f)), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), true); },
  () { BigInt f = BigInt.parse("9223372036854775807"); return bisect(1738, (BigInt c) => (((c).toInt()) == (f)), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775807"), true); },
  () { BigInt f = BigInt.parse("9007199254740993"); return bisect(1739, (BigInt c) => (((c).toInt()) == (f)), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9007199254740993"), true); },
  () { BigInt f = BigInt.parse("9007199254740993"); return bisect(1740, (BigInt c) => (((c).toInt()) == (f)), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9007199254740993"), true); },
  () { double f = 42.0; return bisect(1741, (BigInt c) => (((c).toInt()) * (f)), "*", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), true); },
  () { double f = 9223372036854775807.0; return bisect(1742, (BigInt c) => (((c).toInt()) * (f)), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), true); },
  () { double f = 9223372036854775808.0; return bisect(1743, (BigInt c) => (((c).toInt()) * (f)), "*", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775808"), true); },
  () { double f = 9223372036854775808.0; return bisect(1744, (BigInt c) => (((c).toInt()) < (f)), "<", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775808"), true); },
  () { double f = 9223372036854775808.0; return bisect(1745, (BigInt c) => (((c).toInt()) >= (f)), ">=", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775808"), true); },
  () { double f = 9223372036854775808.0; return bisect(1746, (BigInt c) => (((c).toInt()) == (f)), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775808"), true); },
  () { double f = 9007199254740993.0; return bisect(1747, (BigInt c) => (((c).toInt()) * (f)), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9007199254740993"), true); },
  () { double f = 18446744073709551615.0; return bisect(1748, (BigInt c) => (((c).toInt()) * (f)), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("18446744073709551615"), true); },
  () { int f = 42; return bisect(1755, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), true); },
  () { int f = 42; return bisect(1756, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), true); },
  () { int f = 0; return bisect(1757, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), true); },
  () { int f = 9223372036854775807; return bisect(1758, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775807"), true); },
  () { int f = 9007199254740993; return bisect(1760, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9007199254740993"), true); },
  () { int f = 9007199254740993; return bisect(1761, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9007199254740993"), true); },
  () { double f = 42.0; return bisect(1763, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), true); },
  () { double f = 42.0; return bisect(1764, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), true); },
  () { double f = 0.0; return bisect(1765, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), true); },
  () { double f = 9223372036854775807.0; return bisect(1766, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775807"), true); },
  () { double f = 9223372036854775808.0; return bisect(1767, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775808"), true); },
  () { double f = 9007199254740993.0; return bisect(1768, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9007199254740993"), true); },
  () { double f = 9007199254740993.0; return bisect(1769, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9007199254740993"), true); },
  () { double f = 18446744073709551615.0; return bisect(1770, (BigInt c) => (((c)) == (f)), "==", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("18446744073709551615"), true); },
  () { int f = 42; return bisect(1773, (BigInt c) => (((c).toDouble()) * (f)), "*", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), true); },
  () { int f = 42; return bisect(1774, (BigInt c) => (((c).toDouble()) * (f)), "*", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("42"), true); },
  () { int f = 9223372036854775807; return bisect(1775, (BigInt c) => (((c).toDouble()) * (f)), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), true); },
  () { int f = 9223372036854775807; return bisect(1776, (BigInt c) => (((c).toDouble()) <= (f)), "<=", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775807"), true); },
  () { int f = 9223372036854775807; return bisect(1777, (BigInt c) => (((c).toDouble()) > (f)), ">", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775807"), true); },
  () { int f = 9223372036854775807; return bisect(1778, (BigInt c) => (((c).toDouble()) == (f)), "==", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775807"), true); },
  () { int f = 9007199254740993; return bisect(1779, (BigInt c) => (((c).toDouble()) * (f)), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9007199254740993"), true); },
  () { BigInt f = BigInt.parse("42"); return bisect(1780, (BigInt c) => (((c).toDouble()) == (f)), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), true); },
  () { BigInt f = BigInt.parse("42"); return bisect(1781, (BigInt c) => (((c).toDouble()) == (f)), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), true); },
  () { BigInt f = BigInt.parse("0"); return bisect(1782, (BigInt c) => (((c).toDouble()) == (f)), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), true); },
  () { BigInt f = BigInt.parse("9223372036854775807"); return bisect(1783, (BigInt c) => (((c).toDouble()) == (f)), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775807"), true); },
  () { BigInt f = BigInt.parse("9223372036854775808"); return bisect(1784, (BigInt c) => (((c).toDouble()) == (f)), "==", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775808"), true); },
  () { BigInt f = BigInt.parse("9007199254740993"); return bisect(1785, (BigInt c) => (((c).toDouble()) == (f)), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9007199254740993"), true); },
  () { BigInt f = BigInt.parse("9007199254740993"); return bisect(1786, (BigInt c) => (((c).toDouble()) == (f)), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9007199254740993"), true); },
  () { BigInt f = BigInt.parse("18446744073709551615"); return bisect(1787, (BigInt c) => (((c).toDouble()) == (f)), "==", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("18446744073709551615"), true); },
  () { double f = 42.0; return bisect(1788, (BigInt c) => (((c).toDouble()) * (f)), "*", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), true); },
  () { double f = 42.0; return bisect(1789, (BigInt c) => (((c).toDouble()) * (f)), "*", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("42"), true); },
  () { double f = 9223372036854775807.0; return bisect(1790, (BigInt c) => (((c).toDouble()) * (f)), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), true); },
  () { double f = 9223372036854775807.0; return bisect(1791, (BigInt c) => (((c).toDouble()) <= (f)), "<=", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775807"), true); },
  () { double f = 9223372036854775807.0; return bisect(1792, (BigInt c) => (((c).toDouble()) > (f)), ">", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775807"), true); },
  () { double f = 9223372036854775807.0; return bisect(1793, (BigInt c) => (((c).toDouble()) == (f)), "==", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775807"), true); },
  () { double f = 9223372036854775808.0; return bisect(1794, (BigInt c) => (((c).toDouble()) * (f)), "*", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775808"), true); },
  () { double f = 9223372036854775808.0; return bisect(1795, (BigInt c) => (((c).toDouble()) * (f)), "*", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775808"), true); },
  () { double f = 9223372036854775808.0; return bisect(1796, (BigInt c) => (((c).toDouble()) < (f)), "<", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775808"), true); },
  () { double f = 9223372036854775808.0; return bisect(1797, (BigInt c) => (((c).toDouble()) >= (f)), ">=", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775808"), true); },
  () { double f = 9223372036854775808.0; return bisect(1798, (BigInt c) => (((c).toDouble()) == (f)), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775808"), true); },
  () { double f = 9007199254740993.0; return bisect(1799, (BigInt c) => (((c).toDouble()) * (f)), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9007199254740993"), true); },
  () { double f = 18446744073709551615.0; return bisect(1800, (BigInt c) => (((c).toDouble()) * (f)), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("18446744073709551615"), true); },
  () { int f = 42; return bisect(1813, (BigInt c) => ((f) * ((c).toInt())), "*", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("42"), false); },
  () { int f = 42; return bisect(1814, (BigInt c) => ((f) % ((c).toInt())), "%", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), false); },
  () { int f = 42; return bisect(1815, (BigInt c) => ((f) ~/ ((c).toInt())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), false); },
  () { int f = 0; return bisect(1816, (BigInt c) => ((f) % ((c).toInt())), "%", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), false); },
  () { int f = 0; return bisect(1817, (BigInt c) => ((f) ~/ ((c).toInt())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), false); },
  () { int f = 9223372036854775807; return bisect(1818, (BigInt c) => ((f) * ((c).toInt())), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), false); },
  () { int f = 9223372036854775807; return bisect(1819, (BigInt c) => ((f) % ((c).toInt())), "%", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), false); },
  () { int f = 9223372036854775807; return bisect(1820, (BigInt c) => ((f) ~/ ((c).toInt())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), false); },
  () { int f = 9007199254740993; return bisect(1821, (BigInt c) => ((f) * ((c).toInt())), "*", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9007199254740993"), false); },
  () { int f = 9007199254740993; return bisect(1822, (BigInt c) => ((f) % ((c).toInt())), "%", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9007199254740993"), false); },
  () { int f = 9007199254740993; return bisect(1823, (BigInt c) => ((f) ~/ ((c).toInt())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9007199254740993"), false); },
  () { int f = 42; return bisect(1824, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), false); },
  () { int f = 42; return bisect(1825, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), false); },
  () { int f = 0; return bisect(1826, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), false); },
  () { int f = 9223372036854775807; return bisect(1827, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775807"), false); },
  () { int f = 9007199254740993; return bisect(1828, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9007199254740993"), false); },
  () { int f = 9007199254740993; return bisect(1829, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9007199254740993"), false); },
  () { int f = 42; return bisect(1830, (BigInt c) => ((f) * ((c).toDouble())), "*", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), false); },
  () { int f = 42; return bisect(1831, (BigInt c) => ((f) * ((c).toDouble())), "*", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("42"), false); },
  () { int f = 42; return bisect(1832, (BigInt c) => ((f) ~/ ((c).toDouble())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), false); },
  () { int f = 0; return bisect(1833, (BigInt c) => ((f) ~/ ((c).toDouble())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), false); },
  () { int f = 9223372036854775807; return bisect(1834, (BigInt c) => ((f) * ((c).toDouble())), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), false); },
  () { int f = 9223372036854775807; return bisect(1835, (BigInt c) => ((f) < ((c).toDouble())), "<", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775807"), false); },
  () { int f = 9223372036854775807; return bisect(1836, (BigInt c) => ((f) >= ((c).toDouble())), ">=", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775807"), false); },
  () { int f = 9223372036854775807; return bisect(1837, (BigInt c) => ((f) == ((c).toDouble())), "==", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775807"), false); },
  () { int f = 9223372036854775807; return bisect(1838, (BigInt c) => ((f) ~/ ((c).toDouble())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), false); },
  () { int f = 9007199254740993; return bisect(1839, (BigInt c) => ((f) * ((c).toDouble())), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9007199254740993"), false); },
  () { int f = 9007199254740993; return bisect(1840, (BigInt c) => ((f) ~/ ((c).toDouble())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9007199254740993"), false); },
  () { BigInt f = BigInt.parse("42"); return bisect(1841, (BigInt c) => ((f) == ((c).toInt())), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), false); },
  () { BigInt f = BigInt.parse("42"); return bisect(1842, (BigInt c) => ((f) == ((c).toInt())), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), false); },
  () { BigInt f = BigInt.parse("0"); return bisect(1844, (BigInt c) => ((f) == ((c).toInt())), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), false); },
  () { BigInt f = BigInt.parse("9223372036854775807"); return bisect(1845, (BigInt c) => ((f) == ((c).toInt())), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775807"), false); },
  () { BigInt f = BigInt.parse("9007199254740993"); return bisect(1848, (BigInt c) => ((f) == ((c).toInt())), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9007199254740993"), false); },
  () { BigInt f = BigInt.parse("9007199254740993"); return bisect(1849, (BigInt c) => ((f) == ((c).toInt())), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9007199254740993"), false); },
  () { BigInt f = BigInt.parse("42"); return bisect(1852, (BigInt c) => ((f) % ((c))), "%", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), false); },
  () { BigInt f = BigInt.parse("42"); return bisect(1853, (BigInt c) => ((f) ~/ ((c))), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), false); },
  () { BigInt f = BigInt.parse("0"); return bisect(1854, (BigInt c) => ((f) % ((c))), "%", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), false); },
  () { BigInt f = BigInt.parse("0"); return bisect(1855, (BigInt c) => ((f) ~/ ((c))), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), false); },
  () { BigInt f = BigInt.parse("9223372036854775807"); return bisect(1856, (BigInt c) => ((f) % ((c))), "%", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), false); },
  () { BigInt f = BigInt.parse("9223372036854775807"); return bisect(1857, (BigInt c) => ((f) ~/ ((c))), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), false); },
  () { BigInt f = BigInt.parse("9223372036854775808"); return bisect(1858, (BigInt c) => ((f) % ((c))), "%", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775808"), false); },
  () { BigInt f = BigInt.parse("9223372036854775808"); return bisect(1859, (BigInt c) => ((f) ~/ ((c))), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775808"), false); },
  () { BigInt f = BigInt.parse("9007199254740993"); return bisect(1860, (BigInt c) => ((f) % ((c))), "%", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9007199254740993"), false); },
  () { BigInt f = BigInt.parse("9007199254740993"); return bisect(1861, (BigInt c) => ((f) ~/ ((c))), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9007199254740993"), false); },
  () { BigInt f = BigInt.parse("18446744073709551615"); return bisect(1862, (BigInt c) => ((f) % ((c))), "%", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("18446744073709551615"), false); },
  () { BigInt f = BigInt.parse("18446744073709551615"); return bisect(1863, (BigInt c) => ((f) ~/ ((c))), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("18446744073709551615"), false); },
  () { BigInt f = BigInt.parse("42"); return bisect(1864, (BigInt c) => ((f) == ((c).toDouble())), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), false); },
  () { BigInt f = BigInt.parse("42"); return bisect(1865, (BigInt c) => ((f) == ((c).toDouble())), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), false); },
  () { BigInt f = BigInt.parse("0"); return bisect(1866, (BigInt c) => ((f) == ((c).toDouble())), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), false); },
  () { BigInt f = BigInt.parse("9223372036854775807"); return bisect(1867, (BigInt c) => ((f) == ((c).toDouble())), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775807"), false); },
  () { BigInt f = BigInt.parse("9223372036854775808"); return bisect(1868, (BigInt c) => ((f) == ((c).toDouble())), "==", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775808"), false); },
  () { BigInt f = BigInt.parse("9007199254740993"); return bisect(1869, (BigInt c) => ((f) == ((c).toDouble())), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9007199254740993"), false); },
  () { BigInt f = BigInt.parse("9007199254740993"); return bisect(1870, (BigInt c) => ((f) == ((c).toDouble())), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9007199254740993"), false); },
  () { BigInt f = BigInt.parse("18446744073709551615"); return bisect(1871, (BigInt c) => ((f) == ((c).toDouble())), "==", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("18446744073709551615"), false); },
  () { double f = 42.0; return bisect(1872, (BigInt c) => ((f) * ((c).toInt())), "*", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), false); },
  () { double f = 42.0; return bisect(1873, (BigInt c) => ((f) ~/ ((c).toInt())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), false); },
  () { double f = 0.0; return bisect(1874, (BigInt c) => ((f) ~/ ((c).toInt())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), false); },
  () { double f = 9223372036854775807.0; return bisect(1875, (BigInt c) => ((f) * ((c).toInt())), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), false); },
  () { double f = 9223372036854775807.0; return bisect(1876, (BigInt c) => ((f) ~/ ((c).toInt())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), false); },
  () { double f = 9223372036854775808.0; return bisect(1877, (BigInt c) => ((f) * ((c).toInt())), "*", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775808"), false); },
  () { double f = 9223372036854775808.0; return bisect(1878, (BigInt c) => ((f) <= ((c).toInt())), "<=", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775808"), false); },
  () { double f = 9223372036854775808.0; return bisect(1879, (BigInt c) => ((f) > ((c).toInt())), ">", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775808"), false); },
  () { double f = 9223372036854775808.0; return bisect(1880, (BigInt c) => ((f) == ((c).toInt())), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775808"), false); },
  () { double f = 9223372036854775808.0; return bisect(1881, (BigInt c) => ((f) ~/ ((c).toInt())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775808"), false); },
  () { double f = 9007199254740993.0; return bisect(1882, (BigInt c) => ((f) * ((c).toInt())), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9007199254740993"), false); },
  () { double f = 9007199254740993.0; return bisect(1883, (BigInt c) => ((f) ~/ ((c).toInt())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9007199254740993"), false); },
  () { double f = 18446744073709551615.0; return bisect(1884, (BigInt c) => ((f) * ((c).toInt())), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("18446744073709551615"), false); },
  () { double f = 18446744073709551615.0; return bisect(1885, (BigInt c) => ((f) ~/ ((c).toInt())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("18446744073709551615"), false); },
  () { double f = 42.0; return bisect(1886, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), false); },
  () { double f = 42.0; return bisect(1887, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), false); },
  () { double f = 0.0; return bisect(1888, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), false); },
  () { double f = 9223372036854775807.0; return bisect(1889, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775807"), false); },
  () { double f = 9223372036854775808.0; return bisect(1890, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775808"), false); },
  () { double f = 9007199254740993.0; return bisect(1891, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9007199254740993"), false); },
  () { double f = 9007199254740993.0; return bisect(1892, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9007199254740993"), false); },
  () { double f = 18446744073709551615.0; return bisect(1893, (BigInt c) => ((f) == ((c))), "==", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("18446744073709551615"), false); },
  () { double f = 42.0; return bisect(1894, (BigInt c) => ((f) * ((c).toDouble())), "*", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("42"), false); },
  () { double f = 42.0; return bisect(1895, (BigInt c) => ((f) * ((c).toDouble())), "*", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("42"), false); },
  () { double f = 42.0; return bisect(1896, (BigInt c) => ((f) ~/ ((c).toDouble())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("42"), false); },
  () { double f = 0.0; return bisect(1897, (BigInt c) => ((f) ~/ ((c).toDouble())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("0"), false); },
  () { double f = 9223372036854775807.0; return bisect(1898, (BigInt c) => ((f) * ((c).toDouble())), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), false); },
  () { double f = 9223372036854775807.0; return bisect(1899, (BigInt c) => ((f) < ((c).toDouble())), "<", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775807"), false); },
  () { double f = 9223372036854775807.0; return bisect(1900, (BigInt c) => ((f) >= ((c).toDouble())), ">=", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775807"), false); },
  () { double f = 9223372036854775807.0; return bisect(1901, (BigInt c) => ((f) == ((c).toDouble())), "==", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775807"), false); },
  () { double f = 9223372036854775807.0; return bisect(1902, (BigInt c) => ((f) ~/ ((c).toDouble())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775807"), false); },
  () { double f = 9223372036854775808.0; return bisect(1903, (BigInt c) => ((f) * ((c).toDouble())), "*", BigInt.parse("42"), BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775808"), false); },
  () { double f = 9223372036854775808.0; return bisect(1904, (BigInt c) => ((f) * ((c).toDouble())), "*", BigInt.parse("9223372036854775808"), BigInt.parse("18446744073709551615"), BigInt.parse("9223372036854775808"), false); },
  () { double f = 9223372036854775808.0; return bisect(1905, (BigInt c) => ((f) <= ((c).toDouble())), "<=", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775808"), false); },
  () { double f = 9223372036854775808.0; return bisect(1906, (BigInt c) => ((f) > ((c).toDouble())), ">", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775808"), false); },
  () { double f = 9223372036854775808.0; return bisect(1907, (BigInt c) => ((f) == ((c).toDouble())), "==", BigInt.parse("9007199254740993"), BigInt.parse("9223372036854775807"), BigInt.parse("9223372036854775808"), false); },
  () { double f = 9223372036854775808.0; return bisect(1908, (BigInt c) => ((f) ~/ ((c).toDouble())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9223372036854775808"), false); },
  () { double f = 9007199254740993.0; return bisect(1909, (BigInt c) => ((f) * ((c).toDouble())), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9007199254740993"), false); },
  () { double f = 9007199254740993.0; return bisect(1910, (BigInt c) => ((f) ~/ ((c).toDouble())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("9007199254740993"), false); },
  () { double f = 18446744073709551615.0; return bisect(1911, (BigInt c) => ((f) * ((c).toDouble())), "*", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("18446744073709551615"), false); },
  () { double f = 18446744073709551615.0; return bisect(1912, (BigInt c) => ((f) ~/ ((c).toDouble())), "~/", BigInt.parse("0"), BigInt.parse("42"), BigInt.parse("18446744073709551615"), false); },
];

void main() {
  var total = 0;
  for (var k = 0; k < TARGETS.length; k++) {
    total += TARGETS[k]();
    if ((k + 1) % 25 == 0 || k + 1 == TARGETS.length)
      stderr.writeln("progress ${k + 1}/${TARGETS.length} probes=$total");
  }
  stderr.writeln("DONE targets=${TARGETS.length} probes=$total");
}
