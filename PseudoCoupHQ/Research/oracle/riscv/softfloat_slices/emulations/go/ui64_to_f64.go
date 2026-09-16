package emul


func Emu_ui64_to_f64_rm1(v_arg uint64) uint64 {
	var v_i bool = (v_arg == uint64(0x0))
	var v__n23 bool = (v_i != true)
	var v__m24 uint64 = sfSext1u64(v__n23)
	var v_i2 bool = (int64(v_arg) > int64(-1))
	var v__k1 uint64 = sfCtlz64(v_arg)
	var v_i10 uint64 = v__k1
	var v_i11 uint8 = uint8(v_i10)
	var v_i12 uint8 = (v_i11 + uint8(0xff))
	var v_i19 uint64 = (v_i10 + uint64(0xfffffff5))
	var v_i20 uint64 = (v_i19 & uint64(0xffffffff))
	var v__sh5 uint64 = (v_arg << ((v_i20) & 63))
	var v_i21 uint64 = v__sh5
	var v_i13 uint16 = uint16(v_i12)
	var v_i14 uint16 = (uint16(0x43c) - v_i13)
	var v_i23 uint64 = uint64(v_i12)
	var v__sh6 uint64 = (v_arg << ((v_i23) & 63))
	var v_i24 uint64 = v__sh6
	var v_i15 bool = (v_arg < uint64(0x20000000000000))
	var v__sh3 uint64 = (v_arg >> ((uint64(0xb)) & 63))
	var v_i8 uint64 = (v__sh3 + uint64(0x43d0000000000000))
	var v_i17 uint64 = uint64(v_i14)
	var v__sh4 uint64 = (v_i17 << ((uint64(0x34)) & 63))
	var v_i18 uint64 = v__sh4
	var v_i22 uint64 = (v_i21 + v_i18)
	var v__sh7 uint64 = (v_i24 >> ((uint64(0xa)) & 63))
	var v_i28 bool = (v_i24 < uint64(0x400))
	var v__m9 uint64 = sfSext1u64(v_i28)
	var v__n10 uint64 = (v__m9 ^ uint64(0xffffffffffffffff))
	var v_i31 uint64 = (v_i18 & v__n10)
	var v_i32 uint64 = (v__sh7 + v_i31)
	var v__n11 bool = (v_i2 != true)
	var v__m12 uint64 = sfSext1u64(v__n11)
	var v__a13 uint64 = (v_i8 & v__m12)
	var v__m15 uint64 = sfSext1u64(v_i15)
	var v__a16 uint64 = (v_i22 & v__m15)
	var v__o17 uint64 = (v__a13 | v__a16)
	var v__n18 bool = (v_i15 != true)
	var v__c19 bool = (v__n18 && v_i2)
	var v__m20 uint64 = sfSext1u64(v__c19)
	var v__a21 uint64 = (v_i32 & v__m20)
	var v__o22 uint64 = (v__o17 | v__a21)
	var v__a25 uint64 = (v__o22 & v__m24)
	return v__a25
}
