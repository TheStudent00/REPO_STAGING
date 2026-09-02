
import java.math.BigInteger;
import java.util.*;
import java.util.function.Function;

public class BND {
  static final List<String> EXACT = Arrays.asList(
      "+", "-", "*", "<", "<=", ">", ">=", "==", "!=");

  static Object wantv(String op, BigInteger a, BigInteger b) {
    if (!EXACT.contains(op)) return null;
    switch (op) {
      case "+": return a.add(b);
      case "-": return a.subtract(b);
      case "*": return a.multiply(b);
      case "<": return a.compareTo(b) < 0;
      case "<=": return a.compareTo(b) <= 0;
      case ">": return a.compareTo(b) > 0;
      case ">=": return a.compareTo(b) >= 0;
      case "==": return a.compareTo(b) == 0;
      case "!=": return a.compareTo(b) != 0;
    }
    return null;
  }

  static Object asint(Object r) {
    if (r instanceof Boolean) return r;
    if (r instanceof BigInteger) return r;
    if (r instanceof Short || r instanceof Integer || r instanceof Long)
      return BigInteger.valueOf(((Number) r).longValue());
    if (r instanceof Double || r instanceof Float) {
      double d = ((Number) r).doubleValue();
      if (Double.isNaN(d) || Double.isInfinite(d)) return null;
      if (d != Math.floor(d)) return "NONINT";
      return new java.math.BigDecimal(d).toBigInteger();
    }
    return null;
  }

  static String fidv(Object r, String op, BigInteger a, BigInteger b) {
    Object w = wantv(op, a, b);
    if (w == null) return "na";
    Object g = asint(r);
    if (g == null) return "na";
    if (w instanceof Boolean) {
      if (!(g instanceof Boolean)) return "na";
      return w.equals(g) ? "exact" : "inexact";
    }
    if (g instanceof Boolean) return "na";
    if ("NONINT".equals(g)) return "inexact";
    return ((BigInteger) g).equals((BigInteger) w) ? "exact" : "inexact";
  }

  static String sigv(Function<BigInteger, Object> fn, BigInteger c,
                     String op, BigInteger a, BigInteger b) {
    Object r;
    try { r = fn.apply(c); }
    catch (Throwable t) { return "raise|" + t.getClass().getName() + "|na"; }
    String tn = (r == null) ? "null" : r.getClass().getSimpleName();
    return "answer|" + tn + "|" + fidv(r, op, a, b);
  }

  static int bisect(int tid, Function<BigInteger, Object> fn, String op,
                    BigInteger lov, BigInteger hiv, BigInteger fixed,
                    boolean varyIsLhs) {
    java.util.function.Function<BigInteger, String> s = (c) -> {
      BigInteger a = varyIsLhs ? c : fixed;
      BigInteger b = varyIsLhs ? fixed : c;
      return sigv(fn, c, op, a, b);
    };
    BigInteger lo = lov, hi = hiv;
    String slo = s.apply(lo), shi = s.apply(hi);
    int probes = 2;
    if (slo.equals(shi)) {
      System.out.println("N|" + tid + "|" + slo + "|" + shi);
      return probes;
    }
    TreeSet<String> other = new TreeSet<String>();
    while (hi.subtract(lo).compareTo(BigInteger.ONE) > 0) {
      BigInteger mid = lo.add(hi).shiftRight(1);
      String sm = s.apply(mid); probes++;
      if (sm.equals(slo)) lo = mid;
      else { if (!sm.equals(shi)) other.add(sm); hi = mid; }
    }
    System.out.println("B|" + tid + "|" + lo + "|" + hi + "|" + slo + "|" +
                       shi + "|" + probes + "|" + String.join(";", other));
    return probes;
  }

  static final List<java.util.function.Supplier<Integer>> TARGETS = new ArrayList<>();
  static void reg() {
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2488, (c) -> ((Object)(((short)(c).longValue()) + (f))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2489, (c) -> ((Object)(((short)(c).longValue()) * (f))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2490, (c) -> ((Object)(((short)(c).longValue()) + (f))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2491, (c) -> ((Object)(((short)(c).longValue()) * (f))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2500, (c) -> ((Object)(((int)(c).longValue()) + (f))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2501, (c) -> ((Object)(((int)(c).longValue()) * (f))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2502, (c) -> ((Object)(((int)(c).longValue()) + (f))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2503, (c) -> ((Object)(((int)(c).longValue()) * (f))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { short f = 42; return bisect(2512, (c) -> ((Object)(((c).longValue()) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { short f = 42; return bisect(2513, (c) -> ((Object)(((c).longValue()) * (f))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { int f = 42; return bisect(2514, (c) -> ((Object)(((c).longValue()) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { int f = 42; return bisect(2515, (c) -> ((Object)(((c).longValue()) * (f))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { long f = 42L; return bisect(2516, (c) -> ((Object)(((c).longValue()) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { long f = 42L; return bisect(2517, (c) -> ((Object)(((c).longValue()) * (f))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2518, (c) -> ((Object)(((c).longValue()) + (f))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2519, (c) -> ((Object)(((c).longValue()) * (f))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2520, (c) -> ((Object)(((c).longValue()) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2521, (c) -> ((Object)(((c).longValue()) * (f))), "*", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2522, (c) -> ((Object)(((c).longValue()) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2523, (c) -> ((Object)(((c).longValue()) * (f))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2524, (c) -> ((Object)(((c).longValue()) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2525, (c) -> ((Object)(((c).longValue()) * (f))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2526, (c) -> ((Object)(((c).longValue()) + (f))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2527, (c) -> ((Object)(((c).longValue()) * (f))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2528, (c) -> ((Object)(((c).longValue()) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2529, (c) -> ((Object)(((c).longValue()) * (f))), "*", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2548, (c) -> ((Object)((Integer.valueOf((int)(c).longValue())) + (f))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2549, (c) -> ((Object)((Integer.valueOf((int)(c).longValue())) * (f))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2550, (c) -> ((Object)((Integer.valueOf((int)(c).longValue())) + (f))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2551, (c) -> ((Object)((Integer.valueOf((int)(c).longValue())) * (f))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { short f = 42; return bisect(2560, (c) -> ((Object)((Long.valueOf((c).longValue())) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { short f = 42; return bisect(2561, (c) -> ((Object)((Long.valueOf((c).longValue())) * (f))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { int f = 42; return bisect(2562, (c) -> ((Object)((Long.valueOf((c).longValue())) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { int f = 42; return bisect(2563, (c) -> ((Object)((Long.valueOf((c).longValue())) * (f))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { long f = 42L; return bisect(2564, (c) -> ((Object)((Long.valueOf((c).longValue())) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { long f = 42L; return bisect(2565, (c) -> ((Object)((Long.valueOf((c).longValue())) * (f))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2566, (c) -> ((Object)((Long.valueOf((c).longValue())) + (f))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2567, (c) -> ((Object)((Long.valueOf((c).longValue())) * (f))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2568, (c) -> ((Object)((Long.valueOf((c).longValue())) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2569, (c) -> ((Object)((Long.valueOf((c).longValue())) * (f))), "*", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2570, (c) -> ((Object)((Long.valueOf((c).longValue())) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2571, (c) -> ((Object)((Long.valueOf((c).longValue())) * (f))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2572, (c) -> ((Object)((Long.valueOf((c).longValue())) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2573, (c) -> ((Object)((Long.valueOf((c).longValue())) * (f))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), true); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2574, (c) -> ((Object)((Long.valueOf((c).longValue())) + (f))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2575, (c) -> ((Object)((Long.valueOf((c).longValue())) * (f))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2576, (c) -> ((Object)((Long.valueOf((c).longValue())) == (f))), "==", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2577, (c) -> ((Object)((Long.valueOf((c).longValue())) != (f))), "!=", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2578, (c) -> ((Object)((Long.valueOf((c).longValue())) + (f))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2579, (c) -> ((Object)((Long.valueOf((c).longValue())) * (f))), "*", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2580, (c) -> ((Object)((Long.valueOf((c).longValue())) == (f))), "==", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2581, (c) -> ((Object)((Long.valueOf((c).longValue())) == (f))), "==", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2582, (c) -> ((Object)((Long.valueOf((c).longValue())) != (f))), "!=", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2583, (c) -> ((Object)((Long.valueOf((c).longValue())) != (f))), "!=", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("42"); return bisect(2602, (c) -> ((Object)(((c)) == (f))), "==", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("42"); return bisect(2603, (c) -> ((Object)(((c)) == (f))), "==", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("42"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("42"); return bisect(2604, (c) -> ((Object)(((c)) != (f))), "!=", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("42"); return bisect(2605, (c) -> ((Object)(((c)) != (f))), "!=", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("42"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("0"); return bisect(2606, (c) -> ((Object)(((c)) == (f))), "==", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("0"); return bisect(2607, (c) -> ((Object)(((c)) != (f))), "!=", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9223372036854775807"); return bisect(2608, (c) -> ((Object)(((c)) == (f))), "==", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9223372036854775807"); return bisect(2609, (c) -> ((Object)(((c)) != (f))), "!=", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9223372036854775807"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9223372036854775808"); return bisect(2610, (c) -> ((Object)(((c)) == (f))), "==", new BigInteger("9223372036854775808"), new BigInteger("18446744073709551615"), new BigInteger("9223372036854775808"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9223372036854775808"); return bisect(2611, (c) -> ((Object)(((c)) != (f))), "!=", new BigInteger("9223372036854775808"), new BigInteger("18446744073709551615"), new BigInteger("9223372036854775808"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9007199254740993"); return bisect(2612, (c) -> ((Object)(((c)) == (f))), "==", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9007199254740993"); return bisect(2613, (c) -> ((Object)(((c)) == (f))), "==", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9007199254740993"); return bisect(2614, (c) -> ((Object)(((c)) != (f))), "!=", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9007199254740993"); return bisect(2615, (c) -> ((Object)(((c)) != (f))), "!=", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("18446744073709551615"); return bisect(2616, (c) -> ((Object)(((c)) == (f))), "==", new BigInteger("9223372036854775808"), new BigInteger("18446744073709551615"), new BigInteger("18446744073709551615"), true); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("18446744073709551615"); return bisect(2617, (c) -> ((Object)(((c)) != (f))), "!=", new BigInteger("9223372036854775808"), new BigInteger("18446744073709551615"), new BigInteger("18446744073709551615"), true); });
    TARGETS.add(() -> { short f = 42; return bisect(2618, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 42; return bisect(2619, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 0; return bisect(2620, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { short f = 0; return bisect(2621, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { short f = 42; return bisect(2622, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 42; return bisect(2623, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 0; return bisect(2624, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { short f = 0; return bisect(2625, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { short f = 42; return bisect(2626, (c) -> ((Object)((f) + ((c).longValue()))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 42; return bisect(2627, (c) -> ((Object)((f) * ((c).longValue()))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 42; return bisect(2628, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 42; return bisect(2629, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 0; return bisect(2630, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { short f = 0; return bisect(2631, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { short f = 42; return bisect(2632, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 42; return bisect(2633, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 0; return bisect(2634, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { short f = 0; return bisect(2635, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { short f = 42; return bisect(2636, (c) -> ((Object)((f) + (Long.valueOf((c).longValue())))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 42; return bisect(2637, (c) -> ((Object)((f) * (Long.valueOf((c).longValue())))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 42; return bisect(2638, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 42; return bisect(2639, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { short f = 0; return bisect(2640, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { short f = 0; return bisect(2641, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2642, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2643, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 0; return bisect(2644, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { int f = 0; return bisect(2645, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2646, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2647, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 0; return bisect(2648, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { int f = 0; return bisect(2649, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2650, (c) -> ((Object)((f) + ((c).longValue()))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2651, (c) -> ((Object)((f) * ((c).longValue()))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2652, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2653, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 0; return bisect(2654, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { int f = 0; return bisect(2655, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2656, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2657, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 0; return bisect(2658, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { int f = 0; return bisect(2659, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2660, (c) -> ((Object)((f) + (Long.valueOf((c).longValue())))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2661, (c) -> ((Object)((f) * (Long.valueOf((c).longValue())))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2662, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 42; return bisect(2663, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { int f = 0; return bisect(2664, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { int f = 0; return bisect(2665, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2666, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2667, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 0L; return bisect(2668, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { long f = 0L; return bisect(2669, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2670, (c) -> ((Object)((f) + ((short)(c).longValue()))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2671, (c) -> ((Object)((f) * ((short)(c).longValue()))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2672, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2673, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2674, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2675, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2676, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2677, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 0L; return bisect(2678, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { long f = 0L; return bisect(2679, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2680, (c) -> ((Object)((f) + ((int)(c).longValue()))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2681, (c) -> ((Object)((f) * ((int)(c).longValue()))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2682, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2683, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2684, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2685, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2686, (c) -> ((Object)((f) + ((c).longValue()))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2687, (c) -> ((Object)((f) * ((c).longValue()))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2688, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2689, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 0L; return bisect(2690, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { long f = 0L; return bisect(2691, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2692, (c) -> ((Object)((f) + ((c).longValue()))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2693, (c) -> ((Object)((f) * ((c).longValue()))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2694, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2695, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2696, (c) -> ((Object)((f) + ((c).longValue()))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2697, (c) -> ((Object)((f) * ((c).longValue()))), "*", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2698, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2699, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2700, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2701, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 0L; return bisect(2702, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { long f = 0L; return bisect(2703, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2704, (c) -> ((Object)((f) + (Integer.valueOf((int)(c).longValue())))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2705, (c) -> ((Object)((f) * (Integer.valueOf((int)(c).longValue())))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2706, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2707, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2708, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2709, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2710, (c) -> ((Object)((f) + (Long.valueOf((c).longValue())))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2711, (c) -> ((Object)((f) * (Long.valueOf((c).longValue())))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2712, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 42L; return bisect(2713, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { long f = 0L; return bisect(2714, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { long f = 0L; return bisect(2715, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2716, (c) -> ((Object)((f) + (Long.valueOf((c).longValue())))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2717, (c) -> ((Object)((f) * (Long.valueOf((c).longValue())))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2718, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9223372036854775807L; return bisect(2719, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2720, (c) -> ((Object)((f) + (Long.valueOf((c).longValue())))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2721, (c) -> ((Object)((f) * (Long.valueOf((c).longValue())))), "*", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2722, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { long f = 9007199254740993L; return bisect(2723, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2724, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2725, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 0; return bisect(2726, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Integer f = 0; return bisect(2727, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2728, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2729, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 0; return bisect(2730, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Integer f = 0; return bisect(2731, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2732, (c) -> ((Object)((f) + ((c).longValue()))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2733, (c) -> ((Object)((f) * ((c).longValue()))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2734, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2735, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 0; return bisect(2736, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Integer f = 0; return bisect(2737, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2738, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2739, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 0; return bisect(2740, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Integer f = 0; return bisect(2741, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2742, (c) -> ((Object)((f) + (Long.valueOf((c).longValue())))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2743, (c) -> ((Object)((f) * (Long.valueOf((c).longValue())))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2744, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 42; return bisect(2745, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Integer f = 0; return bisect(2746, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Integer f = 0; return bisect(2747, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2748, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2749, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 0L; return bisect(2750, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Long f = 0L; return bisect(2751, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2752, (c) -> ((Object)((f) + ((short)(c).longValue()))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2753, (c) -> ((Object)((f) * ((short)(c).longValue()))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2754, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2755, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2756, (c) -> ((Object)((f) / ((short)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2757, (c) -> ((Object)((f) % ((short)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2758, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2759, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 0L; return bisect(2760, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Long f = 0L; return bisect(2761, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2762, (c) -> ((Object)((f) + ((int)(c).longValue()))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2763, (c) -> ((Object)((f) * ((int)(c).longValue()))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2764, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2765, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2766, (c) -> ((Object)((f) / ((int)(c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2767, (c) -> ((Object)((f) % ((int)(c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2768, (c) -> ((Object)((f) + ((c).longValue()))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2769, (c) -> ((Object)((f) * ((c).longValue()))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2770, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2771, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 0L; return bisect(2772, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Long f = 0L; return bisect(2773, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2774, (c) -> ((Object)((f) + ((c).longValue()))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2775, (c) -> ((Object)((f) * ((c).longValue()))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2776, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2777, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2778, (c) -> ((Object)((f) + ((c).longValue()))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2779, (c) -> ((Object)((f) * ((c).longValue()))), "*", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2780, (c) -> ((Object)((f) / ((c).longValue()))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2781, (c) -> ((Object)((f) % ((c).longValue()))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2782, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2783, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 0L; return bisect(2784, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Long f = 0L; return bisect(2785, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2786, (c) -> ((Object)((f) + (Integer.valueOf((int)(c).longValue())))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2787, (c) -> ((Object)((f) * (Integer.valueOf((int)(c).longValue())))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2788, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2789, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2790, (c) -> ((Object)((f) / (Integer.valueOf((int)(c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2791, (c) -> ((Object)((f) % (Integer.valueOf((int)(c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2792, (c) -> ((Object)((f) + (Long.valueOf((c).longValue())))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2793, (c) -> ((Object)((f) * (Long.valueOf((c).longValue())))), "*", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2794, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 42L; return bisect(2795, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { Long f = 0L; return bisect(2796, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Long f = 0L; return bisect(2797, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2798, (c) -> ((Object)((f) + (Long.valueOf((c).longValue())))), "+", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2799, (c) -> ((Object)((f) * (Long.valueOf((c).longValue())))), "*", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2800, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2801, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2802, (c) -> ((Object)((f) == (Long.valueOf((c).longValue())))), "==", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9223372036854775807L; return bisect(2803, (c) -> ((Object)((f) != (Long.valueOf((c).longValue())))), "!=", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2804, (c) -> ((Object)((f) + (Long.valueOf((c).longValue())))), "+", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2805, (c) -> ((Object)((f) * (Long.valueOf((c).longValue())))), "*", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2806, (c) -> ((Object)((f) / (Long.valueOf((c).longValue())))), "/", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2807, (c) -> ((Object)((f) % (Long.valueOf((c).longValue())))), "%", new BigInteger("0"), new BigInteger("42"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2808, (c) -> ((Object)((f) == (Long.valueOf((c).longValue())))), "==", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2809, (c) -> ((Object)((f) == (Long.valueOf((c).longValue())))), "==", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2810, (c) -> ((Object)((f) != (Long.valueOf((c).longValue())))), "!=", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { Long f = 9007199254740993L; return bisect(2811, (c) -> ((Object)((f) != (Long.valueOf((c).longValue())))), "!=", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("42"); return bisect(2812, (c) -> ((Object)((f) == ((c)))), "==", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("42"); return bisect(2813, (c) -> ((Object)((f) == ((c)))), "==", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("42"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("42"); return bisect(2814, (c) -> ((Object)((f) != ((c)))), "!=", new BigInteger("0"), new BigInteger("42"), new BigInteger("42"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("42"); return bisect(2815, (c) -> ((Object)((f) != ((c)))), "!=", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("42"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("0"); return bisect(2816, (c) -> ((Object)((f) == ((c)))), "==", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("0"); return bisect(2817, (c) -> ((Object)((f) != ((c)))), "!=", new BigInteger("0"), new BigInteger("42"), new BigInteger("0"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9223372036854775807"); return bisect(2818, (c) -> ((Object)((f) == ((c)))), "==", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9223372036854775807"); return bisect(2819, (c) -> ((Object)((f) != ((c)))), "!=", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9223372036854775807"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9223372036854775808"); return bisect(2820, (c) -> ((Object)((f) == ((c)))), "==", new BigInteger("9223372036854775808"), new BigInteger("18446744073709551615"), new BigInteger("9223372036854775808"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9223372036854775808"); return bisect(2821, (c) -> ((Object)((f) != ((c)))), "!=", new BigInteger("9223372036854775808"), new BigInteger("18446744073709551615"), new BigInteger("9223372036854775808"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9007199254740993"); return bisect(2822, (c) -> ((Object)((f) == ((c)))), "==", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9007199254740993"); return bisect(2823, (c) -> ((Object)((f) == ((c)))), "==", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9007199254740993"); return bisect(2824, (c) -> ((Object)((f) != ((c)))), "!=", new BigInteger("42"), new BigInteger("9007199254740993"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("9007199254740993"); return bisect(2825, (c) -> ((Object)((f) != ((c)))), "!=", new BigInteger("9007199254740993"), new BigInteger("9223372036854775807"), new BigInteger("9007199254740993"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("18446744073709551615"); return bisect(2826, (c) -> ((Object)((f) == ((c)))), "==", new BigInteger("9223372036854775808"), new BigInteger("18446744073709551615"), new BigInteger("18446744073709551615"), false); });
    TARGETS.add(() -> { BigInteger f = new BigInteger("18446744073709551615"); return bisect(2827, (c) -> ((Object)((f) != ((c)))), "!=", new BigInteger("9223372036854775808"), new BigInteger("18446744073709551615"), new BigInteger("18446744073709551615"), false); });
  }

  public static void main(String[] args) {
    reg();
    int total = 0;
    int n = TARGETS.size();
    for (int k = 0; k < n; k++) {
      total += TARGETS.get(k).get();
      if ((k + 1) % 25 == 0 || k + 1 == n)
        System.err.println("progress " + (k + 1) + "/" + n +
                           " probes=" + total);
    }
    System.err.println("DONE targets=" + n + " probes=" + total);
  }
}
