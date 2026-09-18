

public final class ui64_to_f64 {
    public static long ui64_to_f64_rm1(long v_arg) {
        final boolean v_i = (v_arg == 0x0L);
        final boolean v__n23 = (v_i != true);
        final long v__m24 = Sf.sext1l(v__n23);
        final boolean v_i2 = (v_arg > -1L);
        final long v__k1 = Sf.ctlz64(v_arg);
        final long v_i10 = v__k1;
        final int v_i11 = (int)(v_i10 & 0xffL);
        final int v_i12 = ((v_i11 + 0xff) & 0xff);
        final long v_i19 = (v_i10 + 0xfffffff5L);
        final long v_i20 = (v_i19 & 0xffffffffL);
        final long v__sh5 = (v_arg << (int)(v_i20 & 63L));
        final long v_i21 = v__sh5;
        final int v_i13 = (v_i12);
        final int v_i14 = ((0x43c - v_i13) & 0xffff);
        final long v_i23 = ((long)v_i12 & 0xffL);
        final long v__sh6 = (v_arg << (int)(v_i23 & 63L));
        final long v_i24 = v__sh6;
        final boolean v_i15 = (Long.compareUnsigned(v_arg, 0x20000000000000L) < 0);
        final long v__sh3 = (v_arg >>> (int)(0xbL & 63L));
        final long v_i8 = (v__sh3 + 0x43d0000000000000L);
        final long v_i17 = ((long)v_i14 & 0xffffL);
        final long v__sh4 = (v_i17 << (int)(0x34L & 63L));
        final long v_i18 = v__sh4;
        final long v_i22 = (v_i21 + v_i18);
        final long v__sh7 = (v_i24 >>> (int)(0xaL & 63L));
        final boolean v_i28 = (Long.compareUnsigned(v_i24, 0x400L) < 0);
        final long v__m9 = Sf.sext1l(v_i28);
        final long v__n10 = (v__m9 ^ 0xffffffffffffffffL);
        final long v_i31 = (v_i18 & v__n10);
        final long v_i32 = (v__sh7 + v_i31);
        final boolean v__n11 = (v_i2 != true);
        final long v__m12 = Sf.sext1l(v__n11);
        final long v__a13 = (v_i8 & v__m12);
        final long v__m15 = Sf.sext1l(v_i15);
        final long v__a16 = (v_i22 & v__m15);
        final long v__o17 = (v__a13 | v__a16);
        final boolean v__n18 = (v_i15 != true);
        final boolean v__c19 = (v__n18 && v_i2);
        final long v__m20 = Sf.sext1l(v__c19);
        final long v__a21 = (v_i32 & v__m20);
        final long v__o22 = (v__o17 | v__a21);
        final long v__a25 = (v__o22 & v__m24);
        return v__a25;
    }
}
