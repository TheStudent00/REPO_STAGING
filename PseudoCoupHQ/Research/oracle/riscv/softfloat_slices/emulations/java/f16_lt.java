

public final class f16_lt {
    public static boolean f16_lt_rm1(long v_arg, long v_arg1) {
        final int v_i = (int)(v_arg);
        final int v_i2 = (v_i & 0xffff);
        final int v_i3 = (int)(v_arg1);
        final int v_i4 = (v_i3 & 0xffff);
        final int v_i5 = (v_i & 0x7c00);
        final boolean v_i6 = (v_i5 != 0x7c00);
        final int v_i7 = (v_i & 0x3ff);
        final boolean v_i8 = (v_i7 == 0x0);
        final boolean v_i9 = (v_i6 || v_i8);
        final int v_i21 = (v_i3 | v_i);
        final int v_i22 = (v_i21 & 0x7fff);
        final boolean v_i23 = (v_i22 != 0x0);
        final int v_i11 = (v_i3 & 0x7c00);
        final boolean v_i12 = (v_i11 != 0x7c00);
        final int v_i13 = (v_i3 & 0x3ff);
        final boolean v_i14 = (v_i13 == 0x0);
        final boolean v_i15 = (v_i12 || v_i14);
        final boolean v__c5 = (v_i9 && v_i15);
        final boolean v_i17 = (Integer.compareUnsigned(v_i2, 0x7fff) > 0);
        final boolean v_i24 = (v_i17 && v_i23);
        final boolean v_i18 = (Integer.compareUnsigned(v_i4, 0x8000) < 0);
        final boolean v_i19 = (v_i17 != v_i18);
        final boolean v_i26 = (v_i2 != v_i4);
        final boolean v_i27 = (Integer.compareUnsigned(v_i2, v_i4) < 0);
        final boolean v_i28 = (v_i17 != v_i27);
        final boolean v_i29 = (v_i26 && v_i28);
        final boolean v__a3 = (v_i29 && v_i19);
        final boolean v__n1 = (v_i19 != true);
        final boolean v__a2 = (v_i24 && v__n1);
        final boolean v__o4 = (v__a2 || v__a3);
        final boolean v__a6 = (v__o4 && v__c5);
        return v__a6;
    }
}
