package emul


func Emu_i32_to_f64_rm0(v_arg uint32) uint64 {
	var v_i bool = (v_arg == uint32(0x0))
	var v__n7 bool = (v_i != true)
	var v__m8 uint64 = sfSext1u64(v__n7)
	var v__k1 uint32 = sfAbs32(v_arg)
	var v__k2 uint32 = sfCtlz32(v__k1)
	var v_i3 uint32 = v__k2
	var v_i12 uint64 = uint64(v__k1)
	var v_i4 uint32 = (v_i3 + uint32(0x15))
	var v_i8 uint32 = (uint32(0x41d) - v_i3)
	var v_i9 uint64 = uint64(v_i8)
	var v__sh5 uint64 = (v_i9 << ((uint64(0x34)) & 63))
	var v_i13 uint64 = uint64(v_i4)
	var v__sh6 uint64 = (v_i12 << ((v_i13) & 63))
	var v_i14 uint64 = v__sh6
	var v__sh3 uint32 = (v_arg >> ((uint32(0x1f)) & 31))
	var v_i6 uint64 = uint64(v__sh3)
	var v__sh4 uint64 = (v_i6 << ((uint64(0x3f)) & 63))
	var v_i11 uint64 = (v__sh5 | v__sh4)
	var v_i15 uint64 = (v_i11 + v_i14)
	var v__a9 uint64 = (v_i15 & v__m8)
	return v__a9
}
