require_relative 'helpers'


def f16_eq_rm0(v_arg, v_arg1)
  v_i = (v_arg & 0xffffffff)
  v_i2 = (v_arg1 & 0xffffffff)
  v_i3 = (v_i & 0x7c00)
  v_i4 = ((v_i3 != 0x7c00) ? 1 : 0)
  v_i5 = (v_i & 0x3ff)
  v_i6 = ((v_i5 == 0x0) ? 1 : 0)
  v_i7 = (v_i4 | v_i6)
  v_i9 = (v_i2 & 0x7c00)
  v_i10 = ((v_i9 != 0x7c00) ? 1 : 0)
  v_i11 = (v_i2 & 0x3ff)
  v_i12 = ((v_i11 == 0x0) ? 1 : 0)
  v_i13 = (v_i10 | v_i12)
  v__c1 = (v_i7 & v_i13)
  v_i15 = (v_i2 ^ v_i)
  v_i18 = (v_i2 | v_i)
  v_i16 = (v_i15 & 0xffff)
  v_i17 = ((v_i16 == 0x0) ? 1 : 0)
  v_i19 = (v_i18 & 0x7fff)
  v_i20 = ((v_i19 == 0x0) ? 1 : 0)
  v_i21 = (v_i17 | v_i20)
  v__a2 = (v_i21 & v__c1)
  v__a2
end
