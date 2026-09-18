

public final class f64_roundToInt {
    public static long f64_roundToInt_rm0(long v_arg, boolean v_arg1) {
        final long v_i = (v_arg >>> (int)(0x34L & 63L));
        final int v_i2 = (int)(v_i);
        final int v_i3 = (v_i2 & 0x7ff);
        final boolean v_i4 = (Integer.compareUnsigned(v_i3, 0x3ff) < 0);
        final boolean v_i16 = (Integer.compareUnsigned(v_i3, 0x432) > 0);
        final long v_i6 = (v_arg & 0x7fffffffffffffffL);
        final boolean v_i7 = (v_i6 == 0x0L);
        final boolean v_i18 = (v_i3 != 0x7ff);
        final long v_i19 = (v_arg & 0xfffffffffffffL);
        final boolean v_i20 = (v_i19 == 0x0L);
        final boolean v_i21 = (v_i20 || v_i18);
        final long v__m1 = Sf.sext1l(v_i21);
        final long v__a2 = (v_arg & v__m1);
        final long v__n3 = (v__m1 ^ 0xffffffffffffffffL);
        final long v__a4 = (0x7ff8000000000000L & v__n3);
        final long v_spec_select4 = (v__a2 | v__a4);
        final int v_i23 = (0x433 - v_i3);
        final long v_i24 = ((long)v_i23 & 0xffffffffL);
        final long v__sh5 = (0x1L << (int)(v_i24 & 63L));
        final long v_i25 = v__sh5;
        final boolean v_i12 = (v_i3 == 0x3fe);
        final long v_i26 = (v_i25 + 0xffffffffffffffffL);
        final long v__sh6 = (v_i25 >>> (int)(0x1L & 63L));
        final long v_i28 = (v__sh6 + v_arg);
        final long v_i29 = (v_i28 & v_i26);
        final boolean v_i30 = (v_i29 == 0x0L);
        final long v__m7 = Sf.sext1l(v_i30);
        final long v_i31 = (v_i25 ^ 0xffffffffffffffffL);
        final long v__a8 = (v_i31 & v__m7);
        final long v__n9 = (v__m7 ^ 0xffffffffffffffffL);
        final long v_i32 = (v__a8 | v__n9);
        final long v_i33 = (0x0L - v_i25);
        final long v_i34 = (v_i32 & v_i33);
        final long v_i35 = (v_i34 & v_i28);
        final long v_i9 = (v_arg & 0x8000000000000000L);
        final boolean v_i11 = (v_i19 != 0x0L);
        final boolean v_i13 = (v_i11 && v_i12);
        final long v__m11 = Sf.sext1l(v_i13);
        final long v_i14 = (v_i9 | 0x3ff0000000000000L);
        final long v__a12 = (v_i14 & v__m11);
        final long v__n13 = (v__m11 ^ 0xffffffffffffffffL);
        final long v__a14 = (v_i9 & v__n13);
        final long v_spec_select = (v__a12 | v__a14);
        final boolean v__c15 = (v_i7 && v_i4);
        final long v__m16 = Sf.sext1l(v__c15);
        final long v__a17 = (v_arg & v__m16);
        final boolean v__n18 = (v_i7 != true);
        final boolean v__c19 = (v__n18 && v_i4);
        final long v__m20 = Sf.sext1l(v__c19);
        final long v__a21 = (v_spec_select & v__m20);
        final long v__o22 = (v__a17 | v__a21);
        final boolean v__n23 = (v_i4 != true);
        final boolean v__n24 = (v_i16 != true);
        final boolean v__c25 = (v__n23 && v__n24);
        final long v__m26 = Sf.sext1l(v__c25);
        final long v__a27 = (v_i35 & v__m26);
        final long v__o28 = (v__o22 | v__a27);
        final long v__m30 = Sf.sext1l(v_i16);
        final long v__a31 = (v_spec_select4 & v__m30);
        final long v__o32 = (v__o28 | v__a31);
        return v__o32;
    }
}
