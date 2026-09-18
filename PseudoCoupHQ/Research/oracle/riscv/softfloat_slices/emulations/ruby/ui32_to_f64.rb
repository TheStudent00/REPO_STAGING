require_relative 'helpers'


def ui32_to_f64_rm1(v_arg)
  v_i = ((v_arg == 0x0) ? 1 : 0)
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
  v__a6
end
