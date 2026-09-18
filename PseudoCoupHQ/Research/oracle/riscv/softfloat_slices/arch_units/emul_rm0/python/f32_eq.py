from helpers import (sf_udiv, sf_sgn, sf_ctlz, sf_abs,
                     sf_usubsat, sf_fshl)


def f32_eq_rm0(v_arg, v_arg1):
    v_i = (v_arg & 0xffffffff)
    v_i2 = (v_arg1 & 0xffffffff)
    v_i3 = (v_i & 0x7f800000)
    v_i4 = (1 if v_i3 != 0x7f800000 else 0)
    v_i5 = (v_i & 0x7fffff)
    v_i6 = (1 if v_i5 == 0x0 else 0)
    v_i7 = (v_i4 | v_i6)
    v_i9 = (v_i2 & 0x7f800000)
    v_i10 = (1 if v_i9 != 0x7f800000 else 0)
    v_i11 = (v_i2 & 0x7fffff)
    v_i12 = (1 if v_i11 == 0x0 else 0)
    v_i13 = (v_i10 | v_i12)
    v__c1 = (v_i7 & v_i13)
    v_i15 = (1 if v_i == v_i2 else 0)
    v_i16 = (v_i2 | v_i)
    v_i17 = (v_i16 & 0x7fffffff)
    v_i18 = (1 if v_i17 == 0x0 else 0)
    v_i19 = (v_i15 | v_i18)
    v__a2 = (v_i19 & v__c1)
    return v__a2
