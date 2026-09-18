

public final class f32_roundToInt {
    public static long f32_roundToInt_rm0(long v_arg, boolean v_arg1) {
        final int v_i = (int)(v_arg);
        final int v_i2 = (v_i >>> (0x17 & 31));
        final int v_i3 = (v_i2 & 0xff);
        final boolean v_i4 = (Integer.compareUnsigned(v_i3, 0x7f) < 0);
        final boolean v_i16 = (Integer.compareUnsigned(v_i3, 0x95) > 0);
        final int v_i6 = (v_i & 0x7fffffff);
        final boolean v_i7 = (v_i6 == 0x0);
        final boolean v_i18 = (v_i3 != 0xff);
        final int v_i19 = (v_i & 0x7fffff);
        final boolean v_i20 = (v_i19 == 0x0);
        final boolean v_i21 = (v_i20 || v_i18);
        final int v__m1 = Sf.sext1i(v_i21);
        final int v__a2 = (v_i & v__m1);
        final int v__n3 = (v__m1 ^ 0xffffffff);
        final int v__a4 = (0x7fc00000 & v__n3);
        final int v_spec_select4 = (v__a2 | v__a4);
        final int v_i23 = (0x96 - v_i3);
        final int v__sh5 = (0x1 << (v_i23 & 31));
        final int v_i24 = v__sh5;
        final boolean v_i12 = (v_i3 == 0x7e);
        final int v_i25 = (v_i24 + 0xffffffff);
        final int v__sh6 = (v_i24 >>> (0x1 & 31));
        final int v_i27 = (v__sh6 + v_i);
        final int v_i28 = (v_i27 & v_i25);
        final boolean v_i29 = (v_i28 == 0x0);
        final int v__m7 = Sf.sext1i(v_i29);
        final int v_i30 = (v_i24 ^ 0xffffffff);
        final int v__a8 = (v_i30 & v__m7);
        final int v__n9 = (v__m7 ^ 0xffffffff);
        final int v_i31 = (v__a8 | v__n9);
        final int v_i32 = (0x0 - v_i24);
        final int v_i33 = (v_i31 & v_i32);
        final int v_i34 = (v_i33 & v_i27);
        final int v_i9 = (v_i & 0x80000000);
        final boolean v_i11 = (v_i19 != 0x0);
        final boolean v_i13 = (v_i11 && v_i12);
        final int v__m11 = Sf.sext1i(v_i13);
        final int v_i14 = (v_i9 | 0x3f800000);
        final int v__a12 = (v_i14 & v__m11);
        final int v__n13 = (v__m11 ^ 0xffffffff);
        final int v__a14 = (v_i9 & v__n13);
        final int v_spec_select = (v__a12 | v__a14);
        final boolean v__c15 = (v_i7 && v_i4);
        final int v__m16 = Sf.sext1i(v__c15);
        final int v__a17 = (v_i & v__m16);
        final boolean v__n18 = (v_i7 != true);
        final boolean v__c19 = (v__n18 && v_i4);
        final int v__m20 = Sf.sext1i(v__c19);
        final int v__a21 = (v_spec_select & v__m20);
        final int v__o22 = (v__a17 | v__a21);
        final boolean v__n24 = (v_i4 != true);
        final boolean v__n23 = (v_i16 != true);
        final boolean v__c25 = (v__n23 && v__n24);
        final int v__m26 = Sf.sext1i(v__c25);
        final int v__a27 = (v_i34 & v__m26);
        final int v__o28 = (v__o22 | v__a27);
        final int v__m30 = Sf.sext1i(v_i16);
        final int v__a31 = (v_spec_select4 & v__m30);
        final int v__o32 = (v__o28 | v__a31);
        final long v_i36 = ((long)v__o32 & 0xffffffffL);
        return v_i36;
    }
}
