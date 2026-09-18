

public final class f64_roundToInt {
    public static long f64_roundToInt_rm1(long v_arg, boolean v_arg1) {
        final long v_i = (v_arg >>> (int)(0x34L & 63L));
        final int v_i2 = (int)(v_i);
        final int v_i3 = (v_i2 & 0x7ff);
        final boolean v_i4 = (Integer.compareUnsigned(v_i3, 0x3ff) < 0);
        final long v_i6 = (v_arg & 0x7fffffffffffffffL);
        final boolean v_i7 = (v_i6 == 0x0L);
        final long v__m1 = Sf.sext1l(v_i7);
        final long v_i8 = (v_arg & 0x8000000000000000L);
        final long v__a2 = (v_arg & v__m1);
        final long v__n3 = (v__m1 ^ 0xffffffffffffffffL);
        final long v__a4 = (v_i8 & v__n3);
        final long v_spec_select = (v__a2 | v__a4);
        final boolean v_i10 = (Integer.compareUnsigned(v_i3, 0x432) > 0);
        final boolean v_i12 = (v_i3 != 0x7ff);
        final int v_i17 = (0x433 - v_i3);
        final long v_i18 = ((long)v_i17 & 0xffffffffL);
        final long v__sh9 = (0xffffffffffffffffL << (int)(v_i18 & 63L));
        final long v__neg = v__sh9;
        final long v_i19 = (v_arg & v__neg);
        final long v_i13 = (v_arg & 0xfffffffffffffL);
        final boolean v_i14 = (v_i13 == 0x0L);
        final boolean v_i15 = (v_i14 || v_i12);
        final long v__m5 = Sf.sext1l(v_i15);
        final long v__a6 = (v_arg & v__m5);
        final long v__n7 = (v__m5 ^ 0xffffffffffffffffL);
        final long v__a8 = (0x7ff8000000000000L & v__n7);
        final long v_spec_select4 = (v__a6 | v__a8);
        final boolean v__n10 = (v_i10 != true);
        final boolean v__n11 = (v_i4 != true);
        final boolean v__c12 = (v__n10 && v__n11);
        final long v__m13 = Sf.sext1l(v__c12);
        final long v__a14 = (v_i19 & v__m13);
        final long v__m15 = Sf.sext1l(v_i4);
        final long v__a16 = (v_spec_select & v__m15);
        final long v__o17 = (v__a14 | v__a16);
        final long v__m19 = Sf.sext1l(v_i10);
        final long v__a20 = (v_spec_select4 & v__m19);
        final long v__o21 = (v__o17 | v__a20);
        return v__o21;
    }
}
