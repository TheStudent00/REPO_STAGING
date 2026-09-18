

public final class ui32_to_f64 {
    public static long ui32_to_f64_rm1(int v_arg) {
        final boolean v_i = (v_arg == 0x0);
        final boolean v__n4 = (v_i != true);
        final long v__m5 = Sf.sext1l(v__n4);
        final int v__k1 = Sf.ctlz32(v_arg);
        final int v_i2 = v__k1;
        final int v_i3 = (v_i2 + 0x15);
        final int v_i4 = (0x41d - v_i2);
        final long v_i5 = ((long)v_i4 & 0xffffffffL);
        final long v__sh2 = (v_i5 << (int)(0x34L & 63L));
        final long v_i8 = ((long)v_i3 & 0xffffffffL);
        final long v_i7 = ((long)v_arg & 0xffffffffL);
        final long v__sh3 = (v_i7 << (int)(v_i8 & 63L));
        final long v_i9 = v__sh3;
        final long v_i10 = (v__sh2 + v_i9);
        final long v__a6 = (v_i10 & v__m5);
        return v__a6;
    }
}
