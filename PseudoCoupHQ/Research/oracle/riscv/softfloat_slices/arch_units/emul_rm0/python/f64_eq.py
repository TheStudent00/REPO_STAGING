from helpers import (sf_udiv, sf_sgn, sf_ctlz, sf_abs,
                     sf_usubsat, sf_fshl)


def f64_eq_rm0(v_arg, v_arg1):
    v_i = (v_arg & 0x7ff0000000000000)
    v_i2 = (1 if v_i != 0x7ff0000000000000 else 0)
    v_i3 = (v_arg & 0xfffffffffffff)
    v_i4 = (1 if v_i3 == 0x0 else 0)
    v_i5 = (v_i2 | v_i4)
    v_i7 = (v_arg1 & 0x7ff0000000000000)
    v_i8 = (1 if v_i7 != 0x7ff0000000000000 else 0)
    v_i9 = (v_arg1 & 0xfffffffffffff)
    v_i10 = (1 if v_i9 == 0x0 else 0)
    v_i11 = (v_i8 | v_i10)
    v__c1 = (v_i5 & v_i11)
    v_i13 = (1 if v_arg == v_arg1 else 0)
    v_i14 = (v_arg1 | v_arg)
    v_i15 = (v_i14 & 0x7fffffffffffffff)
    v_i16 = (1 if v_i15 == 0x0 else 0)
    v_i17 = (v_i13 | v_i16)
    v__a2 = (v_i17 & v__c1)
    return v__a2
