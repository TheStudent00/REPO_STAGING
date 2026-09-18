

public final class ui32_to_f32 {
    public static long ui32_to_f32_rm1(int v_arg) {
        final boolean v_i = (v_arg == 0x0);
        final boolean v__n23 = (v_i != true);
        final int v__m24 = Sf.sext1i(v__n23);
        final boolean v_i2 = (v_arg > (-1));
        final int v__k1 = Sf.ctlz32(v_arg);
        final int v_i10 = v__k1;
        final int v_i11 = (v_i10 & 0xff);
        final int v_i12 = ((v_i11 + 0xff) & 0xff);
        final int v_i13 = (v_i12);
        final int v_i14 = (v_i12);
        final int v_i15 = ((0x9c - v_i14) & 0xffff);
        final boolean v_i16 = (Integer.compareUnsigned(v_arg, 0x1000000) < 0);
        final int v__sh3 = (v_arg >>> (0x8 & 31));
        final int v_i8 = (v__sh3 + 0x4e800000);
        final int v_i18 = (v_i15);
        final int v__sh4 = (v_i18 << (0x17 & 31));
        final int v_i19 = v__sh4;
        final int v_i20 = (v_i13 + 0xfffffff9);
        final int v__sh5 = (v_arg << (v_i20 & 31));
        final int v_i21 = v__sh5;
        final int v_i22 = (v_i21 + v_i19);
        final int v__sh6 = (v_arg << (v_i13 & 31));
        final int v_i23 = v__sh6;
        final int v__sh7 = (v_i23 >>> (0x7 & 31));
        final boolean v_i27 = (Integer.compareUnsigned(v_i23, 0x80) < 0);
        final int v__m9 = Sf.sext1i(v_i27);
        final int v__n10 = (v__m9 ^ 0xffffffff);
        final int v_i30 = (v_i19 & v__n10);
        final int v_i31 = (v__sh7 + v_i30);
        final boolean v__n11 = (v_i2 != true);
        final int v__m12 = Sf.sext1i(v__n11);
        final int v__a13 = (v_i8 & v__m12);
        final int v__m15 = Sf.sext1i(v_i16);
        final int v__a16 = (v_i22 & v__m15);
        final int v__o17 = (v__a13 | v__a16);
        final boolean v__n18 = (v_i16 != true);
        final boolean v__c19 = (v__n18 && v_i2);
        final int v__m20 = Sf.sext1i(v__c19);
        final int v__a21 = (v_i31 & v__m20);
        final int v__o22 = (v__o17 | v__a21);
        final int v__a25 = (v__o22 & v__m24);
        final long v_i32 = ((long)v__a25 & 0xffffffffL);
        return v_i32;
    }
}
