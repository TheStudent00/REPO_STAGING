import java.math.BigInteger;

/** Support for the java emulations.  Hand written, not generated.
 *
 *  Java has fixed widths and NO unsigned type, so a value is kept as its BIT
 *  PATTERN in the natural signed container and unsignedness lives in these
 *  operations.  The semantics are the Go helpers' semantics, which the
 *  SoftFloat test already passed -- the three don't-care pins of
 *  scripts/emit_emulations.py are made here and nowhere else:
 *
 *    a zero divisor yields zero; ctlz(0) is the bit width; a shift amount is
 *    taken modulo the operand width (which is also Java's own rule).
 *
 *  The 128-bit width is carried by BigInteger rather than by a hi/lo pair.
 *  Two of the sixty-seven operations reach it, so the clarity is worth more
 *  than the speed, and a masked BigInteger cannot get a carry wrong. */
public final class Sf {
    private Sf() { }

    // ------------------------------------------------ signed readings ----
    public static int  s8(int x)  { return (byte)  x; }
    public static int  s16(int x) { return (short) x; }

    // ------------------------------------------------- i1 widening -------
    public static int  b2i(boolean b)     { return b ? 1 : 0; }
    public static long b2l(boolean b)     { return b ? 1L : 0L; }
    public static int  sext1i(boolean b)  { return b ? -1 : 0; }
    public static long sext1l(boolean b)  { return b ? -1L : 0L; }

    // ------------------------------------------------- pinned poison -----
    public static int  udiv8(int a, int b)   { return b == 0 ? 0 : a / b; }
    public static int  udiv16(int a, int b)  { return b == 0 ? 0 : a / b; }
    public static int  udiv32(int a, int b) {
        return b == 0 ? 0 : Integer.divideUnsigned(a, b);
    }
    public static long udiv64(long a, long b) {
        return b == 0L ? 0L : Long.divideUnsigned(a, b);
    }

    // -------------------------------------------------- intrinsics -------
    public static int  ctlz16(int x) {
        return x == 0 ? 16 : Integer.numberOfLeadingZeros(x & 0xffff) - 16;
    }
    public static int  ctlz32(int x)  { return Integer.numberOfLeadingZeros(x); }
    public static long ctlz64(long x) { return Long.numberOfLeadingZeros(x); }

    public static int  abs16(int x)  { return (s16(x) < 0 ? -x : x) & 0xffff; }
    public static int  abs32(int x)  { return x < 0 ? -x : x; }
    public static long abs64(long x) { return x < 0L ? -x : x; }

    public static int usubsat8(int a, int b)  { return a > b ? a - b : 0; }
    public static int usubsat16(int a, int b) { return a > b ? a - b : 0; }
    public static int usubsat32(int a, int b) {
        return Integer.compareUnsigned(a, b) > 0 ? a - b : 0;
    }

    public static long fshl64(long a, long b, long c) {
        int s = (int) (c & 63L);
        return s == 0 ? a : (a << s) | (b >>> (64 - s));
    }
    public static int fshl32(int a, int b, int c) {
        int s = c & 31;
        return s == 0 ? a : (a << s) | (b >>> (32 - s));
    }

    // ------------------------------------------------------- 128 bits ----
    private static final BigInteger M128 =
        BigInteger.ONE.shiftLeft(128).subtract(BigInteger.ONE);

    /** A 128-bit pattern, held non-negative in [0, 2^128). */
    public static final class U128 {
        public final BigInteger v;
        U128(BigInteger x) { this.v = x.and(M128); }
        @Override public boolean equals(Object o) {
            return o instanceof U128 && ((U128) o).v.equals(v);
        }
        @Override public int hashCode() { return v.hashCode(); }
        @Override public String toString() { return v.toString(16); }
    }

    private static BigInteger ub(long x) {          // a long, read unsigned
        BigInteger b = BigInteger.valueOf(x);
        return x < 0 ? b.add(BigInteger.ONE.shiftLeft(64)) : b;
    }

    public static U128 u128(long hi, long lo) {
        return new U128(ub(hi).shiftLeft(64).or(ub(lo)));
    }

    public static U128 u128And(U128 a, U128 b)  { return new U128(a.v.and(b.v)); }
    public static U128 u128Or(U128 a, U128 b)   { return new U128(a.v.or(b.v)); }
    public static U128 u128Xor(U128 a, U128 b)  { return new U128(a.v.xor(b.v)); }
    public static U128 u128Add(U128 a, U128 b)  { return new U128(a.v.add(b.v)); }
    public static U128 u128Sub(U128 a, U128 b)  { return new U128(a.v.subtract(b.v)); }
    public static U128 u128Mul(U128 a, U128 b)  { return new U128(a.v.multiply(b.v)); }
    public static U128 u128Udiv(U128 a, U128 b) {
        return b.v.signum() == 0 ? new U128(BigInteger.ZERO)
                                 : new U128(a.v.divide(b.v));
    }
    public static U128 u128Shl(U128 a, U128 b) {
        return new U128(a.v.shiftLeft(b.v.intValue() & 127));
    }
    public static U128 u128Lshr(U128 a, U128 b) {
        return new U128(a.v.shiftRight(b.v.intValue() & 127));
    }

    public static boolean u128Lo1(U128 a)  { return a.v.testBit(0); }
    public static int     u128Lo8(U128 a)  { return a.v.intValue() & 0xff; }
    public static int     u128Lo16(U128 a) { return a.v.intValue() & 0xffff; }
    public static int     u128Lo32(U128 a) { return a.v.intValue(); }
    public static long    u128Lo64(U128 a) { return a.v.longValue(); }

    public static U128 u128Zext1(boolean b)  { return new U128(b ? BigInteger.ONE : BigInteger.ZERO); }
    public static U128 u128Zext8(int x)      { return new U128(BigInteger.valueOf(x & 0xffL)); }
    public static U128 u128Zext16(int x)     { return new U128(BigInteger.valueOf(x & 0xffffL)); }
    public static U128 u128Zext32(int x)     { return new U128(BigInteger.valueOf(x & 0xffffffffL)); }
    public static U128 u128Zext64(long x)    { return new U128(ub(x)); }

    public static U128 u128Sext1(boolean b)  { return new U128(b ? M128 : BigInteger.ZERO); }
    public static U128 u128Sext8(int x)      { return new U128(BigInteger.valueOf(s8(x))); }
    public static U128 u128Sext16(int x)     { return new U128(BigInteger.valueOf(s16(x))); }
    public static U128 u128Sext32(int x)     { return new U128(BigInteger.valueOf(x)); }
    public static U128 u128Sext64(long x)    { return new U128(BigInteger.valueOf(x)); }

    public static boolean u128Eq(U128 a, U128 b) { return a.v.equals(b.v); }
    public static int u128Ucmp(U128 a, U128 b)   { return a.v.compareTo(b.v); }
    public static int u128Scmp(U128 a, U128 b) {
        return s128(a).compareTo(s128(b));
    }
    private static BigInteger s128(U128 a) {
        return a.v.testBit(127) ? a.v.subtract(BigInteger.ONE.shiftLeft(128))
                                : a.v;
    }
}
