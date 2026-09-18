

public final class f32_to_i64 {
    public static long f32_to_i64_rm1(long v_arg) {
        final int v_i = (int)(v_arg);
        final boolean v_i1 = (v_i < (0));
        final int v_i2 = (v_i >>> (0x17 & 31));
        final int v_i4 = (v_i2 & 0xff);
        final int v_i3 = (v_i & 0x7fffff);
        final int v_i14 = (v_i & 0x7f800000);
        final boolean v_i15 = (v_i14 == 0x0);
        final int v__m1 = Sf.sext1i(v_i15);
        final int v_i5 = (0xbe - v_i4);
        final boolean v_i6 = (Integer.compareUnsigned(v_i4, 0xbe) > 0);
        final int v_i16 = (v_i3 | 0x800000);
        final int v__a2 = (v_i3 & v__m1);
        final int v__n3 = (v__m1 ^ 0xffffffff);
        final int v__a4 = (v_i16 & v__n3);
        final int v_i17 = (v__a2 | v__a4);
        final long v_i18 = ((long)v_i17 & 0xffffffffL);
        final long v__sh5 = (v_i18 << (int)(0x28L & 63L));
        final long v_i19 = v__sh5;
        final boolean v_i9 = (v_i3 != 0x0);
        final boolean v_i20 = (v_i4 == 0xbe);
        final long v__m8 = Sf.sext1l(v_i20);
        final boolean v_i8 = (v_i4 == 0xff);
        final boolean v_i10 = (v_i9 && v_i8);
        final long v__m28 = Sf.sext1l(v_i10);
        final boolean v_i21 = (Integer.compareUnsigned(v_i5, 0x40) < 0);
        final long v_i22 = ((long)v_i5 & 0xffffffffL);
        final long v__sh6 = (v_i19 >>> (int)(v_i22 & 63L));
        final long v_i23 = v__sh6;
        final long v__m7 = Sf.sext1l(v_i21);
        final long v_i24 = (v_i23 & v__m7);
        final long v__a9 = (v_i19 & v__m8);
        final long v__n10 = (v__m8 ^ 0xffffffffffffffffL);
        final long v__a11 = (v_i24 & v__n10);
        final long v_i25 = (v__a9 | v__a11);
        final long v_i26 = (0x0L - v_i25);
        final long v__m12 = Sf.sext1l(v_i1);
        final long v__a13 = (v_i26 & v__m12);
        final long v__n14 = (v__m12 ^ 0xffffffffffffffffL);
        final long v__a15 = (v_i25 & v__n14);
        final long v_i27 = (v__a13 | v__a15);
        final boolean v_i28 = (v_i25 == 0x0L);
        final boolean v_i29 = (v_i27 > -1L);
        final boolean v_i30 = (v_i1 != v_i29);
        final boolean v_i31 = (v_i28 || v_i30);
        final long v__m20 = Sf.sext1l(v_i31);
        final long v__a21 = (v_i27 & v__m20);
        final long v__n22 = (v__m20 ^ 0xffffffffffffffffL);
        final long v__a17 = (0x8000000000000000L & v__m12);
        final long v__a19 = (0x7fffffffffffffffL & v__n14);
        final long v_i32 = (v__a17 | v__a19);
        final long v__a23 = (v_i32 & v__n22);
        final long v_spec_select = (v__a21 | v__a23);
        final long v__a29 = (0x7fffffffffffffffL & v__m28);
        final long v__n30 = (v__m28 ^ 0xffffffffffffffffL);
        final long v__a31 = (v_i32 & v__n30);
        final long v_i12 = (v__a29 | v__a31);
        final long v__m32 = Sf.sext1l(v_i6);
        final long v__a33 = (v_i12 & v__m32);
        final boolean v__n34 = (v_i6 != true);
        final long v__m35 = Sf.sext1l(v__n34);
        final long v__a36 = (v_spec_select & v__m35);
        final long v__o37 = (v__a33 | v__a36);
        return v__o37;
    }
}
