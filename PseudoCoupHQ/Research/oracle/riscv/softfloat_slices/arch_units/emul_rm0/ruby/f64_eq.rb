require_relative 'helpers'


def f64_eq_rm0(v_arg, v_arg1)
  v_i = (v_arg & 0x7ff0000000000000)
  v_i2 = ((v_i != 0x7ff0000000000000) ? 1 : 0)
  v_i3 = (v_arg & 0xfffffffffffff)
  v_i4 = ((v_i3 == 0x0) ? 1 : 0)
  v_i5 = (v_i2 | v_i4)
  v_i7 = (v_arg1 & 0x7ff0000000000000)
  v_i8 = ((v_i7 != 0x7ff0000000000000) ? 1 : 0)
  v_i9 = (v_arg1 & 0xfffffffffffff)
  v_i10 = ((v_i9 == 0x0) ? 1 : 0)
  v_i11 = (v_i8 | v_i10)
  v__c1 = (v_i5 & v_i11)
  v_i13 = ((v_arg == v_arg1) ? 1 : 0)
  v_i14 = (v_arg1 | v_arg)
  v_i15 = (v_i14 & 0x7fffffffffffffff)
  v_i16 = ((v_i15 == 0x0) ? 1 : 0)
  v_i17 = (v_i13 | v_i16)
  v__a2 = (v_i17 & v__c1)
  v__a2
end
