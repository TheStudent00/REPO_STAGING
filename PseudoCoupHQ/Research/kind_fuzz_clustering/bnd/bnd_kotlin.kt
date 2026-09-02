
import java.math.BigInteger
import java.math.BigDecimal

val EXACT = listOf("+", "-", "*", "<", "<=", ">", ">=", "==", "!=")

fun wantv(op: String, a: BigInteger, b: BigInteger): Any? = when (op) {
  "+" -> a.add(b)
  "-" -> a.subtract(b)
  "*" -> a.multiply(b)
  "<" -> a.compareTo(b) < 0
  "<=" -> a.compareTo(b) <= 0
  ">" -> a.compareTo(b) > 0
  ">=" -> a.compareTo(b) >= 0
  "==" -> a.compareTo(b) == 0
  "!=" -> a.compareTo(b) != 0
  else -> null
}

fun asint(r: Any?): Any? = when (r) {
  is Boolean -> r
  is BigInteger -> r
  is Byte, is Short, is Int, is Long -> BigInteger.valueOf((r as Number).toLong())
  is ULong -> BigInteger(r.toString())
  is UInt -> BigInteger(r.toString())
  is Double -> if (r.isNaN() || r.isInfinite()) null
               else if (r != Math.floor(r)) "NONINT" else BigDecimal(r).toBigInteger()
  is Float -> asint(r.toDouble())
  else -> null
}

fun fidv(r: Any?, op: String, a: BigInteger, b: BigInteger): String {
  val w = wantv(op, a, b) ?: return "na"
  val g = asint(r) ?: return "na"
  if (w is Boolean) {
    if (g !is Boolean) return "na"
    return if (w == g) "exact" else "inexact"
  }
  if (g is Boolean) return "na"
  if (g == "NONINT") return "inexact"
  return if ((g as BigInteger) == (w as BigInteger)) "exact" else "inexact"
}

fun sigv(fn: (BigInteger) -> Any?, c: BigInteger, op: String,
         a: BigInteger, b: BigInteger): String {
  val r: Any?
  try { r = fn(c) }
  catch (t: Throwable) { return "raise|" + t.javaClass.name + "|na" }
  val tn = if (r == null) "null" else r!!::class.simpleName
  return "answer|" + tn + "|" + fidv(r, op, a, b)
}

fun bisect(tid: Int, fn: (BigInteger) -> Any?, op: String,
           lov: BigInteger, hiv: BigInteger, fixed: BigInteger,
           varyIsLhs: Boolean): Int {
  fun s(c: BigInteger): String {
    val a = if (varyIsLhs) c else fixed
    val b = if (varyIsLhs) fixed else c
    return sigv(fn, c, op, a, b)
  }
  var lo = lov; var hi = hiv
  val slo = s(lo); val shi = s(hi)
  var probes = 2
  if (slo == shi) { println("N|$tid|$slo|$shi"); return probes }
  val other = sortedSetOf<String>()
  while (hi.subtract(lo) > BigInteger.ONE) {
    val mid = lo.add(hi).shiftRight(1)
    val sm = s(mid); probes++
    if (sm == slo) lo = mid
    else { if (sm != shi) other.add(sm); hi = mid }
  }
  println("B|$tid|$lo|$hi|$slo|$shi|$probes|" + other.joinToString(";"))
  return probes
}

val TARGETS: List<() -> Int> = listOf(
  { val f: Long = 9223372036854775807L; bisect(2308, { c -> (((c).toInt()) + (f)) as Any? }, "+", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), true) },
  { val f: Long = 9223372036854775807L; bisect(2309, { c -> (((c).toInt()) * (f)) as Any? }, "*", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), true) },
  { val f: Int = 42; bisect(2318, { c -> (((c).toLong()) + (f)) as Any? }, "+", BigInteger("9007199254740993"), BigInteger("9223372036854775807"), BigInteger("42"), true) },
  { val f: Int = 42; bisect(2319, { c -> (((c).toLong()) * (f)) as Any? }, "*", BigInteger("9007199254740993"), BigInteger("9223372036854775807"), BigInteger("42"), true) },
  { val f: Long = 42L; bisect(2320, { c -> (((c).toLong()) + (f)) as Any? }, "+", BigInteger("9007199254740993"), BigInteger("9223372036854775807"), BigInteger("42"), true) },
  { val f: Long = 42L; bisect(2321, { c -> (((c).toLong()) * (f)) as Any? }, "*", BigInteger("9007199254740993"), BigInteger("9223372036854775807"), BigInteger("42"), true) },
  { val f: Long = 9223372036854775807L; bisect(2322, { c -> (((c).toLong()) + (f)) as Any? }, "+", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), true) },
  { val f: Long = 9223372036854775807L; bisect(2323, { c -> (((c).toLong()) * (f)) as Any? }, "*", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), true) },
  { val f: Long = 9007199254740993L; bisect(2324, { c -> (((c).toLong()) + (f)) as Any? }, "+", BigInteger("9007199254740993"), BigInteger("9223372036854775807"), BigInteger("9007199254740993"), true) },
  { val f: Long = 9007199254740993L; bisect(2325, { c -> (((c).toLong()) * (f)) as Any? }, "*", BigInteger("42"), BigInteger("9007199254740993"), BigInteger("9007199254740993"), true) },
  { val f: BigInteger = BigInteger("42"); bisect(2344, { c -> (((c)) - (f)) as Any? }, "-", BigInteger("0"), BigInteger("42"), BigInteger("42"), true) },
  { val f: BigInteger = BigInteger("9223372036854775807"); bisect(2345, { c -> (((c)) - (f)) as Any? }, "-", BigInteger("9007199254740993"), BigInteger("9223372036854775807"), BigInteger("9223372036854775807"), true) },
  { val f: BigInteger = BigInteger("9007199254740993"); bisect(2346, { c -> (((c)) - (f)) as Any? }, "-", BigInteger("42"), BigInteger("9007199254740993"), BigInteger("9007199254740993"), true) },
  { val f: BigInteger = BigInteger("18446744073709551615"); bisect(2347, { c -> (((c)) - (f)) as Any? }, "-", BigInteger("9223372036854775808"), BigInteger("18446744073709551615"), BigInteger("18446744073709551615"), true) },
  { val f: Int = 42; bisect(2350, { c -> ((f) / ((c).toInt())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("42"), false) },
  { val f: Int = 42; bisect(2351, { c -> ((f) % ((c).toInt())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("42"), false) },
  { val f: Int = 0; bisect(2352, { c -> ((f) / ((c).toInt())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("0"), false) },
  { val f: Int = 0; bisect(2353, { c -> ((f) % ((c).toInt())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("0"), false) },
  { val f: Int = 42; bisect(2354, { c -> ((f) + ((c).toLong())) as Any? }, "+", BigInteger("9007199254740993"), BigInteger("9223372036854775807"), BigInteger("42"), false) },
  { val f: Int = 42; bisect(2355, { c -> ((f) * ((c).toLong())) as Any? }, "*", BigInteger("9007199254740993"), BigInteger("9223372036854775807"), BigInteger("42"), false) },
  { val f: Int = 42; bisect(2356, { c -> ((f) / ((c).toLong())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("42"), false) },
  { val f: Int = 42; bisect(2357, { c -> ((f) % ((c).toLong())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("42"), false) },
  { val f: Int = 0; bisect(2358, { c -> ((f) / ((c).toLong())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("0"), false) },
  { val f: Int = 0; bisect(2359, { c -> ((f) % ((c).toLong())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("0"), false) },
  { val f: Long = 42L; bisect(2360, { c -> ((f) / ((c).toInt())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("42"), false) },
  { val f: Long = 42L; bisect(2361, { c -> ((f) % ((c).toInt())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("42"), false) },
  { val f: Long = 0L; bisect(2362, { c -> ((f) / ((c).toInt())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("0"), false) },
  { val f: Long = 0L; bisect(2363, { c -> ((f) % ((c).toInt())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("0"), false) },
  { val f: Long = 9223372036854775807L; bisect(2364, { c -> ((f) + ((c).toInt())) as Any? }, "+", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), false) },
  { val f: Long = 9223372036854775807L; bisect(2365, { c -> ((f) * ((c).toInt())) as Any? }, "*", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), false) },
  { val f: Long = 9223372036854775807L; bisect(2366, { c -> ((f) / ((c).toInt())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), false) },
  { val f: Long = 9223372036854775807L; bisect(2367, { c -> ((f) % ((c).toInt())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), false) },
  { val f: Long = 9007199254740993L; bisect(2368, { c -> ((f) / ((c).toInt())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("9007199254740993"), false) },
  { val f: Long = 9007199254740993L; bisect(2369, { c -> ((f) % ((c).toInt())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("9007199254740993"), false) },
  { val f: Long = 42L; bisect(2370, { c -> ((f) + ((c).toLong())) as Any? }, "+", BigInteger("9007199254740993"), BigInteger("9223372036854775807"), BigInteger("42"), false) },
  { val f: Long = 42L; bisect(2371, { c -> ((f) * ((c).toLong())) as Any? }, "*", BigInteger("9007199254740993"), BigInteger("9223372036854775807"), BigInteger("42"), false) },
  { val f: Long = 42L; bisect(2372, { c -> ((f) / ((c).toLong())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("42"), false) },
  { val f: Long = 42L; bisect(2373, { c -> ((f) % ((c).toLong())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("42"), false) },
  { val f: Long = 0L; bisect(2374, { c -> ((f) / ((c).toLong())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("0"), false) },
  { val f: Long = 0L; bisect(2375, { c -> ((f) % ((c).toLong())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("0"), false) },
  { val f: Long = 9223372036854775807L; bisect(2376, { c -> ((f) + ((c).toLong())) as Any? }, "+", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), false) },
  { val f: Long = 9223372036854775807L; bisect(2377, { c -> ((f) * ((c).toLong())) as Any? }, "*", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), false) },
  { val f: Long = 9223372036854775807L; bisect(2378, { c -> ((f) / ((c).toLong())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), false) },
  { val f: Long = 9223372036854775807L; bisect(2379, { c -> ((f) % ((c).toLong())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), false) },
  { val f: Long = 9007199254740993L; bisect(2380, { c -> ((f) + ((c).toLong())) as Any? }, "+", BigInteger("9007199254740993"), BigInteger("9223372036854775807"), BigInteger("9007199254740993"), false) },
  { val f: Long = 9007199254740993L; bisect(2381, { c -> ((f) * ((c).toLong())) as Any? }, "*", BigInteger("42"), BigInteger("9007199254740993"), BigInteger("9007199254740993"), false) },
  { val f: Long = 9007199254740993L; bisect(2382, { c -> ((f) / ((c).toLong())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("9007199254740993"), false) },
  { val f: Long = 9007199254740993L; bisect(2383, { c -> ((f) % ((c).toLong())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("9007199254740993"), false) },
  { val f: ULong = 42uL; bisect(2384, { c -> ((f) / ((c).toLong().toULong())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("42"), false) },
  { val f: ULong = 42uL; bisect(2385, { c -> ((f) % ((c).toLong().toULong())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("42"), false) },
  { val f: ULong = 0uL; bisect(2386, { c -> ((f) / ((c).toLong().toULong())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("0"), false) },
  { val f: ULong = 0uL; bisect(2387, { c -> ((f) % ((c).toLong().toULong())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("0"), false) },
  { val f: ULong = 9223372036854775807uL; bisect(2388, { c -> ((f) / ((c).toLong().toULong())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), false) },
  { val f: ULong = 9223372036854775807uL; bisect(2389, { c -> ((f) % ((c).toLong().toULong())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), false) },
  { val f: ULong = 9223372036854775808uL; bisect(2390, { c -> ((f) / ((c).toLong().toULong())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775808"), false) },
  { val f: ULong = 9223372036854775808uL; bisect(2391, { c -> ((f) % ((c).toLong().toULong())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775808"), false) },
  { val f: ULong = 9007199254740993uL; bisect(2392, { c -> ((f) / ((c).toLong().toULong())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("9007199254740993"), false) },
  { val f: ULong = 9007199254740993uL; bisect(2393, { c -> ((f) % ((c).toLong().toULong())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("9007199254740993"), false) },
  { val f: ULong = 18446744073709551615uL; bisect(2394, { c -> ((f) / ((c).toLong().toULong())) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("18446744073709551615"), false) },
  { val f: ULong = 18446744073709551615uL; bisect(2395, { c -> ((f) % ((c).toLong().toULong())) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("18446744073709551615"), false) },
  { val f: BigInteger = BigInteger("42"); bisect(2396, { c -> ((f) - ((c))) as Any? }, "-", BigInteger("42"), BigInteger("9007199254740993"), BigInteger("42"), false) },
  { val f: BigInteger = BigInteger("42"); bisect(2397, { c -> ((f) / ((c))) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("42"), false) },
  { val f: BigInteger = BigInteger("42"); bisect(2398, { c -> ((f) % ((c))) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("42"), false) },
  { val f: BigInteger = BigInteger("0"); bisect(2399, { c -> ((f) - ((c))) as Any? }, "-", BigInteger("0"), BigInteger("42"), BigInteger("0"), false) },
  { val f: BigInteger = BigInteger("0"); bisect(2400, { c -> ((f) / ((c))) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("0"), false) },
  { val f: BigInteger = BigInteger("0"); bisect(2401, { c -> ((f) % ((c))) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("0"), false) },
  { val f: BigInteger = BigInteger("9223372036854775807"); bisect(2402, { c -> ((f) / ((c))) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), false) },
  { val f: BigInteger = BigInteger("9223372036854775807"); bisect(2403, { c -> ((f) % ((c))) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775807"), false) },
  { val f: BigInteger = BigInteger("9223372036854775808"); bisect(2404, { c -> ((f) - ((c))) as Any? }, "-", BigInteger("9223372036854775808"), BigInteger("18446744073709551615"), BigInteger("9223372036854775808"), false) },
  { val f: BigInteger = BigInteger("9223372036854775808"); bisect(2405, { c -> ((f) / ((c))) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775808"), false) },
  { val f: BigInteger = BigInteger("9223372036854775808"); bisect(2406, { c -> ((f) % ((c))) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("9223372036854775808"), false) },
  { val f: BigInteger = BigInteger("9007199254740993"); bisect(2407, { c -> ((f) - ((c))) as Any? }, "-", BigInteger("9007199254740993"), BigInteger("9223372036854775807"), BigInteger("9007199254740993"), false) },
  { val f: BigInteger = BigInteger("9007199254740993"); bisect(2408, { c -> ((f) / ((c))) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("9007199254740993"), false) },
  { val f: BigInteger = BigInteger("9007199254740993"); bisect(2409, { c -> ((f) % ((c))) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("9007199254740993"), false) },
  { val f: BigInteger = BigInteger("18446744073709551615"); bisect(2410, { c -> ((f) / ((c))) as Any? }, "/", BigInteger("0"), BigInteger("42"), BigInteger("18446744073709551615"), false) },
  { val f: BigInteger = BigInteger("18446744073709551615"); bisect(2411, { c -> ((f) % ((c))) as Any? }, "%", BigInteger("0"), BigInteger("42"), BigInteger("18446744073709551615"), false) }
)

fun main() {
  var total = 0
  val n = TARGETS.size
  for (k in 0 until n) {
    total += TARGETS[k]()
    if ((k + 1) % 25 == 0 || k + 1 == n)
      System.err.println("progress ${k + 1}/$n probes=$total")
  }
  System.err.println("DONE targets=$n probes=$total")
}
