

public final class f16_roundToInt {
    public static long f16_roundToInt_rm1(long v_arg, boolean v_arg1) {
        final int v_i = (int)(v_arg & 0xffffL);
        final int v_i2 = (int)(v_arg);
        final int v_i3 = (v_i2 >>> (0xa & 31));
        final int v_i4 = (v_i3 & 0x1f);
        final int v_i14 = (v_i2 & 0x3ff);
        final boolean v_i15 = (v_i14 == 0x0);
        final boolean v_i5 = (Integer.compareUnsigned(v_i4, 0xf) < 0);
        final boolean v_i11 = (Integer.compareUnsigned(v_i4, 0x18) > 0);
        final long v_i7 = (v_arg & 0x7fffL);
        final boolean v_i8 = (v_i7 == 0x0L);
        final int v__m1 = Sf.sext1i(v_i8);
        final int v_i9 = (v_i & 0x8000);
        final int v__a2 = (v_i & v__m1);
        final int v__n3 = (v__m1 ^ 0xffff);
        final int v__a4 = (v_i9 & v__n3);
        final int v_spec_select = (v__a2 | v__a4);
        final boolean v_i13 = (v_i4 != 0x1f);
        final boolean v_i16 = (v_i15 || v_i13);
        final int v__m5 = Sf.sext1i(v_i16);
        final int v_i18 = (0x19 - v_i4);
        final int v__sh9 = (0xffff << (v_i18 & 31));
        final int v_i19 = v__sh9;
        final int v_i20 = (v_i19 & 0xffff);
        final int v_i21 = (v_i & v_i20);
        final int v__a6 = (v_i & v__m5);
        final int v__n7 = (v__m5 ^ 0xffff);
        final int v__a8 = (0x7e00 & v__n7);
        final int v_spec_select4 = (v__a6 | v__a8);
        final boolean v__n10 = (v_i11 != true);
        final boolean v__n11 = (v_i5 != true);
        final boolean v__c12 = (v__n10 && v__n11);
        final int v__m13 = Sf.sext1i(v__c12);
        final int v__a14 = (v_i21 & v__m13);
        final int v__m15 = Sf.sext1i(v_i5);
        final int v__a16 = (v_spec_select & v__m15);
        final int v__o17 = (v__a14 | v__a16);
        final int v__m19 = Sf.sext1i(v_i11);
        final int v__a20 = (v_spec_select4 & v__m19);
        final int v__o21 = (v__o17 | v__a20);
        final long v_i23 = ((long)v__o21 & 0xffffL);
        return v_i23;
    }
}
