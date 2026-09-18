

public final class f64_eq {
    public static boolean f64_eq_rm0(long v_arg, long v_arg1) {
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
        final boolean v__c1 = (v_i5 && v_i11);
        final boolean v_i13 = (v_arg == v_arg1);
        final long v_i14 = (v_arg1 | v_arg);
        final long v_i15 = (v_i14 & 0x7fffffffffffffffL);
        final boolean v_i16 = (v_i15 == 0x0L);
        final boolean v_i17 = (v_i13 || v_i16);
        final boolean v__a2 = (v_i17 && v__c1);
        return v__a2;
    }
}
