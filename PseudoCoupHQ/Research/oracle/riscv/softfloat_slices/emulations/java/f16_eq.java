

public final class f16_eq {
    public static boolean f16_eq_rm1(long v_arg, long v_arg1) {
        final int v_i = (int)(v_arg);
        final int v_i2 = (int)(v_arg1);
        final int v_i3 = (v_i & 0x7c00);
        final boolean v_i4 = (v_i3 != 0x7c00);
        final int v_i5 = (v_i & 0x3ff);
        final boolean v_i6 = (v_i5 == 0x0);
        final boolean v_i7 = (v_i4 || v_i6);
        final int v_i9 = (v_i2 & 0x7c00);
        final boolean v_i10 = (v_i9 != 0x7c00);
        final int v_i11 = (v_i2 & 0x3ff);
        final boolean v_i12 = (v_i11 == 0x0);
        final boolean v_i13 = (v_i10 || v_i12);
        final boolean v__c1 = (v_i7 && v_i13);
        final int v_i15 = (v_i2 ^ v_i);
        final int v_i18 = (v_i2 | v_i);
        final int v_i16 = (v_i15 & 0xffff);
        final boolean v_i17 = (v_i16 == 0x0);
        final int v_i19 = (v_i18 & 0x7fff);
        final boolean v_i20 = (v_i19 == 0x0);
        final boolean v_i21 = (v_i17 || v_i20);
        final boolean v__a2 = (v_i21 && v__c1);
        return v__a2;
    }
}
