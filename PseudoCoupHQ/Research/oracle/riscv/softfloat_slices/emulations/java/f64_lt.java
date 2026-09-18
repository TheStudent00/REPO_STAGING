

public final class f64_lt {
    public static boolean f64_lt_rm1(long v_arg, long v_arg1) {
        final long v_i = (v_arg & 0x7ff0000000000000L);
        final boolean v_i2 = (v_i != 0x7ff0000000000000L);
        final long v_i3 = (v_arg & 0xfffffffffffffL);
        final boolean v_i4 = (v_i3 == 0x0L);
        final boolean v_i5 = (v_i2 || v_i4);
        final long v_i7 = (v_arg1 & 0x7ff0000000000000L);
        final boolean v_i8 = (v_i7 != 0x7ff0000000000000L);
        final long v_i9 = (v_arg1 & 0xfffffffffffffL);
        final boolean v_i10 = (v_i9 == 0x0L);
        final boolean v_i11 = (v_i8 || v_i10);
        final boolean v__c5 = (v_i5 && v_i11);
        final long v_i13 = (v_arg1 ^ v_arg);
        final boolean v_i14 = (v_i13 > -1L);
        final boolean v_i16 = (v_arg < 0L);
        final long v_i17 = (v_arg1 | v_arg);
        final long v_i18 = (v_i17 & 0x7fffffffffffffffL);
        final boolean v_i19 = (v_i18 != 0x0L);
        final boolean v_i20 = (v_i16 && v_i19);
        final boolean v_i22 = (v_arg != v_arg1);
        final boolean v_i23 = (Long.compareUnsigned(v_arg, v_arg1) < 0);
        final boolean v_i25 = (v_i16 != v_i23);
        final boolean v_i26 = (v_i22 && v_i25);
        final boolean v__a3 = (v_i26 && v_i14);
        final boolean v__n1 = (v_i14 != true);
        final boolean v__a2 = (v_i20 && v__n1);
        final boolean v__o4 = (v__a2 || v__a3);
        final boolean v__a6 = (v__o4 && v__c5);
        return v__a6;
    }
}
