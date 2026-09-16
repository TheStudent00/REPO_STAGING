package emul


func Emu_ui32_to_f64_rm1(v_arg uint32) uint64 {
	var v_i bool = (v_arg == uint32(0x0))
	var v__n4 bool = (v_i != true)
	var v__m5 uint64 = sfSext1u64(v__n4)
	var v__k1 uint32 = sfCtlz32(v_arg)
	var v_i2 uint32 = v__k1
	var v_i3 uint32 = (v_i2 + uint32(0x15))
	var v_i4 uint32 = (uint32(0x41d) - v_i2)
	var v_i5 uint64 = uint64(v_i4)
	var v__sh2 uint64 = (v_i5 << ((uint64(0x34)) & 63))
	var v_i8 uint64 = uint64(v_i3)
	var v_i7 uint64 = uint64(v_arg)
	var v__sh3 uint64 = (v_i7 << ((v_i8) & 63))
	var v_i9 uint64 = v__sh3
	var v_i10 uint64 = (v__sh2 + v_i9)
	var v__a6 uint64 = (v_i10 & v__m5)
	return v__a6
}
