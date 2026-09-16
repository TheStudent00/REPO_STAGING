package emul


func Emu_ui32_to_f32_rm1(v_arg uint32) uint64 {
	var v_i bool = (v_arg == uint32(0x0))
	var v__n23 bool = (v_i != true)
	var v__m24 uint32 = sfSext1u32(v__n23)
	var v_i2 bool = (int32(v_arg) > int32(-1))
	var v__k1 uint32 = sfCtlz32(v_arg)
	var v_i10 uint32 = v__k1
	var v_i11 uint8 = uint8(v_i10)
	var v_i12 uint8 = (v_i11 + uint8(0xff))
	var v_i13 uint32 = uint32(v_i12)
	var v_i14 uint16 = uint16(v_i12)
	var v_i15 uint16 = (uint16(0x9c) - v_i14)
	var v_i16 bool = (v_arg < uint32(0x1000000))
	var v__sh3 uint32 = (v_arg >> ((uint32(0x8)) & 31))
	var v_i8 uint32 = (v__sh3 + uint32(0x4e800000))
	var v_i18 uint32 = uint32(v_i15)
	var v__sh4 uint32 = (v_i18 << ((uint32(0x17)) & 31))
	var v_i19 uint32 = v__sh4
	var v_i20 uint32 = (v_i13 + uint32(0xfffffff9))
	var v__sh5 uint32 = (v_arg << ((v_i20) & 31))
	var v_i21 uint32 = v__sh5
	var v_i22 uint32 = (v_i21 + v_i19)
	var v__sh6 uint32 = (v_arg << ((v_i13) & 31))
	var v_i23 uint32 = v__sh6
	var v__sh7 uint32 = (v_i23 >> ((uint32(0x7)) & 31))
	var v_i27 bool = (v_i23 < uint32(0x80))
	var v__m9 uint32 = sfSext1u32(v_i27)
	var v__n10 uint32 = (v__m9 ^ uint32(0xffffffff))
	var v_i30 uint32 = (v_i19 & v__n10)
	var v_i31 uint32 = (v__sh7 + v_i30)
	var v__n11 bool = (v_i2 != true)
	var v__m12 uint32 = sfSext1u32(v__n11)
	var v__a13 uint32 = (v_i8 & v__m12)
	var v__m15 uint32 = sfSext1u32(v_i16)
	var v__a16 uint32 = (v_i22 & v__m15)
	var v__o17 uint32 = (v__a13 | v__a16)
	var v__n18 bool = (v_i16 != true)
	var v__c19 bool = (v__n18 && v_i2)
	var v__m20 uint32 = sfSext1u32(v__c19)
	var v__a21 uint32 = (v_i31 & v__m20)
	var v__o22 uint32 = (v__o17 | v__a21)
	var v__a25 uint32 = (v__o22 & v__m24)
	var v_i32 uint64 = uint64(v__a25)
	return v_i32
}
