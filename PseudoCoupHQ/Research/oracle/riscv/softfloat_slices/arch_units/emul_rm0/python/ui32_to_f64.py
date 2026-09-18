from helpers import (sf_udiv, sf_sgn, sf_ctlz, sf_abs,
                     sf_usubsat, sf_fshl)


def ui32_to_f64_rm0(v_arg):
    v_i = (1 if v_arg == 0x0 else 0)
    v__n4 = (v_i ^ 0x1)
    v__m5 = (sf_sgn(v__n4, 0x1) & 0xffffffffffffffff)
    v__k1 = sf_ctlz(v_arg, 0x20)
    v_i2 = v__k1
    v_i3 = ((v_i2 + 0x15) & 0xffffffff)
    v_i4 = ((0x41d - v_i2) & 0xffffffff)
    v_i5 = (v_i4)
    v__sh2 = ((v_i5 << (0x34 & 0x3f)) & 0xffffffffffffffff)
    v_i8 = (v_i3)
    v_i7 = (v_arg)
    v__sh3 = ((v_i7 << (v_i8 & 0x3f)) & 0xffffffffffffffff)
    v_i9 = v__sh3
    v_i10 = ((v__sh2 + v_i9) & 0xffffffffffffffff)
    v__a6 = (v_i10 & v__m5)
    return v__a6
