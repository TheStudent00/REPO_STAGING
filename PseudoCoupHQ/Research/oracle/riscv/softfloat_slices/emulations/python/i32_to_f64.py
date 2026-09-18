from helpers import (sf_udiv, sf_sgn, sf_ctlz, sf_abs,
                     sf_usubsat, sf_fshl)


def i32_to_f64_rm1(v_arg):
    v_i = (1 if v_arg == 0x0 else 0)
    v__n7 = (v_i ^ 0x1)
    v__m8 = (sf_sgn(v__n7, 0x1) & 0xffffffffffffffff)
    v__k1 = sf_abs(v_arg, 0x20)
    v__k2 = sf_ctlz(v__k1, 0x20)
    v_i3 = v__k2
    v_i12 = (v__k1)
    v_i4 = ((v_i3 + 0x15) & 0xffffffff)
    v_i8 = ((0x41d - v_i3) & 0xffffffff)
    v_i9 = (v_i8)
    v__sh5 = ((v_i9 << (0x34 & 0x3f)) & 0xffffffffffffffff)
    v_i13 = (v_i4)
    v__sh6 = ((v_i12 << (v_i13 & 0x3f)) & 0xffffffffffffffff)
    v_i14 = v__sh6
    v__sh3 = (v_arg >> (0x1f & 0x1f))
    v_i6 = (v__sh3)
    v__sh4 = ((v_i6 << (0x3f & 0x3f)) & 0xffffffffffffffff)
    v_i11 = (v__sh5 | v__sh4)
    v_i15 = ((v_i11 + v_i14) & 0xffffffffffffffff)
    v__a9 = (v_i15 & v__m8)
    return v__a9
