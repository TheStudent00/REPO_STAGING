package emul


func Emu_f64_lt_quiet_rm1(v_arg uint64, v_arg1 uint64) bool {
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
	var v__c5 bool = (v_i5 && v_i11)
	var v_i13 uint64 = (v_arg1 ^ v_arg)
	var v_i14 bool = (int64(v_i13) > int64(-1))
	var v_i16 bool = (int64(v_arg) < int64(0))
	var v_i17 uint64 = (v_arg1 | v_arg)
	var v_i18 uint64 = (v_i17 & uint64(0x7fffffffffffffff))
	var v_i19 bool = (v_i18 != uint64(0x0))
	var v_i20 bool = (v_i16 && v_i19)
	var v_i22 bool = (v_arg != v_arg1)
	var v_i23 bool = (v_arg < v_arg1)
	var v_i25 bool = (v_i16 != v_i23)
	var v_i26 bool = (v_i22 && v_i25)
	var v__a3 bool = (v_i26 && v_i14)
	var v__n1 bool = (v_i14 != true)
	var v__a2 bool = (v_i20 && v__n1)
	var v__o4 bool = (v__a2 || v__a3)
	var v__a6 bool = (v__o4 && v__c5)
	return v__a6
}
