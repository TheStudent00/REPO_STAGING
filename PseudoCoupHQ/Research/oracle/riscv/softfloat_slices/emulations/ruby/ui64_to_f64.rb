require_relative 'helpers'


def ui64_to_f64_rm1(v_arg)
  v_i = ((v_arg == 0x0) ? 1 : 0)
  v__n23 = (v_i ^ 0x1)
  v__m24 = (sf_sgn(v__n23, 0x1) & 0xffffffffffffffff)
  v_i2 = ((sf_sgn(v_arg, 0x40) > (-1)) ? 1 : 0)
  v__k1 = sf_ctlz(v_arg, 0x40)
  v_i10 = v__k1
  v_i11 = (v_i10 & 0xff)
  v_i12 = ((v_i11 + 0xff) & 0xff)
  v_i19 = ((v_i10 + 0xfffffff5) & 0xffffffffffffffff)
  v_i20 = (v_i19 & 0xffffffff)
  v__sh5 = ((v_arg << (v_i20 & 0x3f)) & 0xffffffffffffffff)
  v_i21 = v__sh5
  v_i13 = (v_i12)
  v_i14 = ((0x43c - v_i13) & 0xffff)
  v_i23 = (v_i12)
  v__sh6 = ((v_arg << (v_i23 & 0x3f)) & 0xffffffffffffffff)
  v_i24 = v__sh6
  v_i15 = ((v_arg < 0x20000000000000) ? 1 : 0)
  v__sh3 = (v_arg >> (0xb & 0x3f))
  v_i8 = ((v__sh3 + 0x43d0000000000000) & 0xffffffffffffffff)
  v_i17 = (v_i14)
  v__sh4 = ((v_i17 << (0x34 & 0x3f)) & 0xffffffffffffffff)
  v_i18 = v__sh4
  v_i22 = ((v_i21 + v_i18) & 0xffffffffffffffff)
  v__sh7 = (v_i24 >> (0xa & 0x3f))
  v_i28 = ((v_i24 < 0x400) ? 1 : 0)
  v__m9 = (sf_sgn(v_i28, 0x1) & 0xffffffffffffffff)
  v__n10 = (v__m9 ^ 0xffffffffffffffff)
  v_i31 = (v_i18 & v__n10)
  v_i32 = ((v__sh7 + v_i31) & 0xffffffffffffffff)
  v__n11 = (v_i2 ^ 0x1)
  v__m12 = (sf_sgn(v__n11, 0x1) & 0xffffffffffffffff)
  v__a13 = (v_i8 & v__m12)
  v__m15 = (sf_sgn(v_i15, 0x1) & 0xffffffffffffffff)
  v__a16 = (v_i22 & v__m15)
  v__o17 = (v__a13 | v__a16)
  v__n18 = (v_i15 ^ 0x1)
  v__c19 = (v__n18 & v_i2)
  v__m20 = (sf_sgn(v__c19, 0x1) & 0xffffffffffffffff)
  v__a21 = (v_i32 & v__m20)
  v__o22 = (v__o17 | v__a21)
  v__a25 = (v__o22 & v__m24)
  v__a25
end
