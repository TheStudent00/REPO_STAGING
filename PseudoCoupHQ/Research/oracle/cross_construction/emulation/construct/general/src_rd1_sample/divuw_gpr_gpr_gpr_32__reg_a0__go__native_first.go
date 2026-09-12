// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of divuw_gpr_gpr_gpr_32__reg_a0__go__native_first.
//   Concat(If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If
package main

//go:noinline
func emu_divuw_gpr_gpr_gpr_32__reg_a0__go__native_first(a uint32, b uint32) uint64 {
	var v0 uint32 = uint32(a)
	var v1 uint32 = uint32(b)
	var v2 uint32 = (uint32((uint32(v1)) / (uint32(v0))))
	var v3 bool = ((uint32(v0)) == (uint32(uint32(0x0))))
	var v4 uint32 = 0
	if v3 {
		v4 = uint32(0xffffffff)
	} else {
		v4 = v2
	}
	var v6 uint32 = 0
	if v3 {
		v6 = uint32(0x1)
	} else {
		var v5 uint32 = ((uint32((uint32(v2)) >> 31)) & uint32(0x1))
		v6 = v5
	}
	var v7 uint64 = (uint64(((uint64(v6)) << 63) | ((uint64(v6)) << 62) | ((uint64(v6)) << 61) | ((uint64(v6)) << 60) | ((uint64(v6)) << 59) | ((uint64(v6)) << 58) | ((uint64(v6)) << 57) | ((uint64(v6)) << 56) | ((uint64(v6)) << 55) | ((uint64(v6)) << 54) | ((uint64(v6)) << 53) | ((uint64(v6)) << 52) | ((uint64(v6)) << 51) | ((uint64(v6)) << 50) | ((uint64(v6)) << 49) | ((uint64(v6)) << 48) | ((uint64(v6)) << 47) | ((uint64(v6)) << 46) | ((uint64(v6)) << 45) | ((uint64(v6)) << 44) | ((uint64(v6)) << 43) | ((uint64(v6)) << 42) | ((uint64(v6)) << 41) | ((uint64(v6)) << 40) | ((uint64(v6)) << 39) | ((uint64(v6)) << 38) | ((uint64(v6)) << 37) | ((uint64(v6)) << 36) | ((uint64(v6)) << 35) | ((uint64(v6)) << 34) | ((uint64(v6)) << 33) | ((uint64(v6)) << 32) | (uint64(v4))))
	return uint64(v7)
}

var g0 uint32
var g1 uint32
var sink interface{}

func main() {
	sink = emu_divuw_gpr_gpr_gpr_32__reg_a0__go__native_first(g0, g1)
	_ = sink
}
