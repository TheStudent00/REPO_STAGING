

public final class f32_roundToInt {
    public static long f32_roundToInt_rm1(long v_arg, boolean v_arg1) {
        final int v_i = (int)(v_arg);
        final int v_i2 = (v_i >>> (0x17 & 31));
        final int v_i3 = (v_i2 & 0xff);
        final boolean v_i4 = (Integer.compareUnsigned(v_i3, 0x7f) < 0);
        final int v_i6 = (v_i & 0x7fffffff);
        final boolean v_i7 = (v_i6 == 0x0);
        final int v__m1 = Sf.sext1i(v_i7);
        final int v_i8 = (v_i & 0x80000000);
        final int v__a2 = (v_i & v__m1);
        final int v__n3 = (v__m1 ^ 0xffffffff);
        final int v__a4 = (v_i8 & v__n3);
        final int v_spec_select = (v__a2 | v__a4);
        final boolean v_i10 = (Integer.compareUnsigned(v_i3, 0x95) > 0);
        final boolean v_i12 = (v_i3 != 0xff);
        final int v_i17 = (0x96 - v_i3);
        final int v__sh9 = (0xffffffff << (v_i17 & 31));
        final int v__neg = v__sh9;
        final int v_i18 = (v__neg & v_i);
        final int v_i13 = (v_i & 0x7fffff);
        final boolean v_i14 = (v_i13 == 0x0);
        final boolean v_i15 = (v_i14 || v_i12);
        final int v__m5 = Sf.sext1i(v_i15);
        final int v__a6 = (v_i & v__m5);
        final int v__n7 = (v__m5 ^ 0xffffffff);
        final int v__a8 = (0x7fc00000 & v__n7);
        final int v_spec_select4 = (v__a6 | v__a8);
        final boolean v__n10 = (v_i10 != true);
        final boolean v__n11 = (v_i4 != true);
        final boolean v__c12 = (v__n10 && v__n11);
        final int v__m13 = Sf.sext1i(v__c12);
        final int v__a14 = (v_i18 & v__m13);
        final int v__m15 = Sf.sext1i(v_i4);
        final int v__a16 = (v_spec_select & v__m15);
        final int v__o17 = (v__a14 | v__a16);
        final int v__m19 = Sf.sext1i(v_i10);
        final int v__a20 = (v_spec_select4 & v__m19);
        final int v__o21 = (v__o17 | v__a20);
        final long v_i20 = ((long)v__o21 & 0xffffffffL);
        return v_i20;
    }
}
