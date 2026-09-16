package emul


func Emu_f32_eq_rm1(v_arg uint64, v_arg1 uint64) bool {
	var v_i uint32 = uint32(v_arg)
	var v_i2 uint32 = uint32(v_arg1)
	var v_i3 uint32 = (v_i & uint32(0x7f800000))
	var v_i4 bool = (v_i3 != uint32(0x7f800000))
	var v_i5 uint32 = (v_i & uint32(0x7fffff))
	var v_i6 bool = (v_i5 == uint32(0x0))
	var v_i7 bool = (v_i4 || v_i6)
	var v_i9 uint32 = (v_i2 & uint32(0x7f800000))
	var v_i10 bool = (v_i9 != uint32(0x7f800000))
	var v_i11 uint32 = (v_i2 & uint32(0x7fffff))
	var v_i12 bool = (v_i11 == uint32(0x0))
	var v_i13 bool = (v_i10 || v_i12)
	var v__c1 bool = (v_i7 && v_i13)
	var v_i15 bool = (v_i == v_i2)
	var v_i16 uint32 = (v_i2 | v_i)
	var v_i17 uint32 = (v_i16 & uint32(0x7fffffff))
	var v_i18 bool = (v_i17 == uint32(0x0))
	var v_i19 bool = (v_i15 || v_i18)
	var v__a2 bool = (v_i19 && v__c1)
	return v__a2
}
