

public final class i64_to_f64 {
    public static long i64_to_f64_rm1(long v_arg) {
        final long v_i = (v_arg & 0x7fffffffffffffffL);
        final boolean v_i1 = (v_i == 0x0L);
        final boolean v_i3 = (v_arg < 0L);
        final long v__m1 = Sf.sext1l(v_i3);
        final long v_i4 = (0xc3e0000000000000L & v__m1);
        final long v__k2 = Sf.abs64(v_arg);
        final boolean v_i7 = (v_arg == 0x0L);
        final long v__k3 = Sf.ctlz64(v__k2);
        final long v_i9 = v__k3;
        final int v_i10 = (int)(v_i9 & 0xffL);
        final int v_i11 = ((v_i10 + 0xff) & 0xff);
        final boolean v__n4 = (v_i7 != true);
        final int v__m5 = Sf.sext1i(v__n4);
        final int v__a6 = (v_i11 & v__m5);
        final int v__m7 = Sf.sext1i(v_i7);
        final int v__a8 = (0x3f & v__m7);
        final int v__o9 = (v__a6 | v__a8);
        final long v__m14 = Sf.sext1l(v_i7);
        final long v__n15 = (v__m14 ^ 0xffffffffffffffffL);
        final boolean v__n10 = (v_i1 != true);
        final long v__m22 = Sf.sext1l(v_i1);
        final long v__a23 = (v_i4 & v__m22);
        final int v__m11 = Sf.sext1i(v__n10);
        final int v__a12 = (v__o9 & v__m11);
        final int v_i14 = (Sf.s8(v__a12));
        final int v_i15 = (Sf.s8(v__a12) & 0xffff);
        final int v_i16 = ((0x43c - v_i15) & 0xffff);
        final boolean v_i17 = (Sf.s8(v__a12) > (9));
        final long v_i19 = ((long)v_i16 & 0xffffL);
        final long v__sh13 = (v_i19 << (int)(0x34L & 63L));
        final long v_i21 = v__sh13;
        final long v_i22 = (v_i21 & v__n15);
        final long v_i20 = (v_arg & 0x8000000000000000L);
        final int v_i23 = (v_i14 + 0xfffffff6);
        final long v_i24 = ((long)v_i23 & 0xffffffffL);
        final long v__sh16 = (v__k2 << (int)(v_i24 & 63L));
        final long v_i25 = v__sh16;
        final long v_i26 = (v_i25 + v_i20);
        final long v_i27 = (v_i26 + v_i22);
        final long v_i28 = ((long)v_i14 & 0xffffffffL);
        final long v__sh17 = (v__k2 << (int)(v_i28 & 63L));
        final long v_i29 = v__sh17;
        final long v__sh18 = (v_i29 >>> (int)(0xaL & 63L));
        final boolean v_i33 = (Long.compareUnsigned(v_i29, 0x400L) < 0);
        final long v__m20 = Sf.sext1l(v_i33);
        final long v__n21 = (v__m20 ^ 0xffffffffffffffffL);
        final long v_i37 = (v_i21 & v__n21);
        final long v_i38 = (v__sh18 | v_i20);
        final long v_i39 = (v_i38 + v_i37);
        final boolean v__c24 = (v__n10 && v_i17);
        final long v__m25 = Sf.sext1l(v__c24);
        final long v__a26 = (v_i27 & v__m25);
        final long v__o27 = (v__a23 | v__a26);
        final boolean v__n28 = (v_i17 != true);
        final boolean v__c29 = (v__n10 && v__n28);
        final long v__m30 = Sf.sext1l(v__c29);
        final long v__a31 = (v_i39 & v__m30);
        final long v__o32 = (v__o27 | v__a31);
        return v__o32;
    }
}
