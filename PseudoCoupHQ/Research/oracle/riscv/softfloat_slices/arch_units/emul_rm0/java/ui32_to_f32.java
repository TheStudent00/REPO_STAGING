

public final class ui32_to_f32 {
    public static long ui32_to_f32_rm0(int v_arg) {
        final boolean v_i = (v_arg == 0x0);
        final boolean v__n25 = (v_i != true);
        final int v__m26 = Sf.sext1i(v__n25);
        final boolean v_i2 = (v_arg > (-1));
        final int v__k1 = Sf.ctlz32(v_arg);
        final int v_i17 = v__k1;
        final int v_i18 = (v_i17 & 0xff);
        final int v_i19 = ((v_i18 + 0xff) & 0xff);
        final int v_i20 = (v_i19);
        final int v_i21 = (v_i19);
        final int v_i22 = ((0x9c - v_i21) & 0xffff);
        final boolean v_i23 = (Integer.compareUnsigned(v_arg, 0x1000000) < 0);
        final int v__sh2 = (v_arg >>> (0x1 & 31));
        final int v_i4 = (v_arg & 0x1);
        final int v_i5 = (v__sh2 + 0x40);
        final int v__sh3 = (v_i5 >>> (0x7 & 31));
        final int v__masked = (v__sh2 & 0x7f);
        final int v_i7 = (v__masked | v_i4);
        final boolean v_i9 = (v_i7 == 0x40);
        final int v_i10 = Sf.b2i(v_i9);
        final int v_i11 = (v_i10 ^ 0xffffffff);
        final int v_i12 = (v__sh3 & v_i11);
        final boolean v_i13 = (v_i12 == 0x0);
        final int v__m4 = Sf.sext1i(v_i13);
        final int v__n5 = (v__m4 ^ 0xffffffff);
        final int v_i14 = (0x4e800000 & v__n5);
        final int v_i15 = (v_i12 + v_i14);
        final int v_i25 = (v_i22);
        final int v__sh6 = (v_i25 << (0x17 & 31));
        final int v_i26 = v__sh6;
        final int v_i27 = (v_i20 + 0xfffffff9);
        final int v__sh7 = (v_arg << (v_i27 & 31));
        final int v_i28 = v__sh7;
        final int v_i29 = (v_i28 + v_i26);
        final int v__sh8 = (v_arg << (v_i20 & 31));
        final int v_i30 = v__sh8;
        final int v_i31 = (v_i30 + 0x40);
        final int v__sh9 = (v_i31 >>> (0x7 & 31));
        final int v_i33 = (v_i30 & 0x7f);
        final boolean v_i35 = (v_i33 == 0x40);
        final int v_i36 = Sf.b2i(v_i35);
        final int v_i37 = (v_i36 ^ 0xffffffff);
        final int v_i38 = (v__sh9 & v_i37);
        final boolean v_i39 = (v_i38 == 0x0);
        final int v__m11 = Sf.sext1i(v_i39);
        final int v__n12 = (v__m11 ^ 0xffffffff);
        final int v_i42 = (v_i26 & v__n12);
        final int v_i43 = (v_i38 + v_i42);
        final boolean v__n13 = (v_i2 != true);
        final int v__m14 = Sf.sext1i(v__n13);
        final int v__a15 = (v_i15 & v__m14);
        final int v__m17 = Sf.sext1i(v_i23);
        final int v__a18 = (v_i29 & v__m17);
        final int v__o19 = (v__a15 | v__a18);
        final boolean v__n20 = (v_i23 != true);
        final boolean v__c21 = (v_i2 && v__n20);
        final int v__m22 = Sf.sext1i(v__c21);
        final int v__a23 = (v_i43 & v__m22);
        final int v__o24 = (v__o19 | v__a23);
        final int v__a27 = (v__o24 & v__m26);
        final long v_i44 = ((long)v__a27 & 0xffffffffL);
        return v_i44;
    }
}
