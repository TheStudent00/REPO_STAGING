

public final class f32_lt {
    public static boolean f32_lt_rm0(long v_arg, long v_arg1) {
        final int v_i = (int)(v_arg);
        final int v_i2 = (int)(v_arg1);
        final int v_i3 = (v_i & 0x7f800000);
        final boolean v_i4 = (v_i3 != 0x7f800000);
        final int v_i5 = (v_i & 0x7fffff);
        final boolean v_i6 = (v_i5 == 0x0);
        final boolean v_i7 = (v_i4 || v_i6);
        final int v_i9 = (v_i2 & 0x7f800000);
        final boolean v_i10 = (v_i9 != 0x7f800000);
        final int v_i11 = (v_i2 & 0x7fffff);
        final boolean v_i12 = (v_i11 == 0x0);
        final boolean v_i13 = (v_i10 || v_i12);
        final boolean v__c5 = (v_i7 && v_i13);
        final int v_i15 = (v_i2 ^ v_i);
        final boolean v_i16 = (v_i15 > (-1));
        final boolean v_i18 = (v_i < (0));
        final int v_i19 = (v_i2 | v_i);
        final int v_i20 = (v_i19 & 0x7fffffff);
        final boolean v_i21 = (v_i20 != 0x0);
        final boolean v_i22 = (v_i18 && v_i21);
        final boolean v_i24 = (v_i != v_i2);
        final boolean v_i25 = (Integer.compareUnsigned(v_i, v_i2) < 0);
        final boolean v_i27 = (v_i18 != v_i25);
        final boolean v_i28 = (v_i24 && v_i27);
        final boolean v__a3 = (v_i28 && v_i16);
        final boolean v__n1 = (v_i16 != true);
        final boolean v__a2 = (v_i22 && v__n1);
        final boolean v__o4 = (v__a2 || v__a3);
        final boolean v__a6 = (v__o4 && v__c5);
        return v__a6;
    }
}
