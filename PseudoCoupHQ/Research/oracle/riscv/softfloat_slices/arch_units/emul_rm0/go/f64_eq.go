package emul


func Emu_f64_eq_rm0(v_arg uint64, v_arg1 uint64) bool {
	var v_i uint64 = (v_arg & uint64(0x7ff0000000000000))
	var v_i2 bool = (v_i != uint64(0x7ff0000000000000))
	var v_i3 uint64 = (v_arg & uint64(0xfffffffffffff))
	var v_i4 bool = (v_i3 == uint64(0x0))
	var v_i5 bool = (v_i2 || v_i4)
	var v_i7 uint64 = (v_arg1 & uint64(0x7ff0000000000000))
	var v_i8 bool = (v_i7 != uint64(0x7ff0000000000000))
	var v_i9 uint64 = (v_arg1 & uint64(0xfffffffffffff))
	var v_i10 bool = (v_i9 == uint64(0x0))
	var v_i11 bool = (v_i8 || v_i10)
	var v__c1 bool = (v_i5 && v_i11)
	var v_i13 bool = (v_arg == v_arg1)
	var v_i14 uint64 = (v_arg1 | v_arg)
	var v_i15 uint64 = (v_i14 & uint64(0x7fffffffffffffff))
	var v_i16 bool = (v_i15 == uint64(0x0))
	var v_i17 bool = (v_i13 || v_i16)
	var v__a2 bool = (v_i17 && v__c1)
	return v__a2
}
