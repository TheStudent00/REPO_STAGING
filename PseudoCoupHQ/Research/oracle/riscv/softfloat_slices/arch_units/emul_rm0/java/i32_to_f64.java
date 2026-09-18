

public final class i32_to_f64 {
    public static long i32_to_f64_rm0(int v_arg) {
        final boolean v_i = (v_arg == 0x0);
        final boolean v__n7 = (v_i != true);
        final long v__m8 = Sf.sext1l(v__n7);
        final int v__k1 = Sf.abs32(v_arg);
        final int v__k2 = Sf.ctlz32(v__k1);
        final int v_i3 = v__k2;
        final long v_i12 = ((long)v__k1 & 0xffffffffL);
        final int v_i4 = (v_i3 + 0x15);
        final int v_i8 = (0x41d - v_i3);
        final long v_i9 = ((long)v_i8 & 0xffffffffL);
        final long v__sh5 = (v_i9 << (int)(0x34L & 63L));
        final long v_i13 = ((long)v_i4 & 0xffffffffL);
        final long v__sh6 = (v_i12 << (int)(v_i13 & 63L));
        final long v_i14 = v__sh6;
        final int v__sh3 = (v_arg >>> (0x1f & 31));
        final long v_i6 = ((long)v__sh3 & 0xffffffffL);
        final long v__sh4 = (v_i6 << (int)(0x3fL & 63L));
        final long v_i11 = (v__sh5 | v__sh4);
        final long v_i15 = (v_i11 + v_i14);
        final long v__a9 = (v_i15 & v__m8);
        return v__a9;
    }
}
