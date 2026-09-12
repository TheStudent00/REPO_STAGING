// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of divuw_gpr_gpr_same_32__reg_a0__go__native_first.
//   Concat(If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, 1, Extract(31, 31, bvudiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_divuw_gpr_gpr_same_32__reg_a0__go__native_first(a uint32) uint64 {
	var v0 uint32 = uint32(a)
	var v1 uint32 = (uint32((uint32(v0)) / (uint32(v0))))
	var v2 bool = ((uint32(v0)) == (uint32(uint32(0x0))))
	var v3 uint32 = sel32(v2, uint32(uint32(0xffffffff)), uint32(v1))
	var v4 uint32 = ((uint32((uint32(v1)) >> 31)) & uint32(0x1))
	var v5 uint32 = sel32(v2, uint32(uint32(0x1)), uint32(v4))
	var v6 uint64 = (uint64(((uint64(v5)) << 63) | ((uint64(v5)) << 62) | ((uint64(v5)) << 61) | ((uint64(v5)) << 60) | ((uint64(v5)) << 59) | ((uint64(v5)) << 58) | ((uint64(v5)) << 57) | ((uint64(v5)) << 56) | ((uint64(v5)) << 55) | ((uint64(v5)) << 54) | ((uint64(v5)) << 53) | ((uint64(v5)) << 52) | ((uint64(v5)) << 51) | ((uint64(v5)) << 50) | ((uint64(v5)) << 49) | ((uint64(v5)) << 48) | ((uint64(v5)) << 47) | ((uint64(v5)) << 46) | ((uint64(v5)) << 45) | ((uint64(v5)) << 44) | ((uint64(v5)) << 43) | ((uint64(v5)) << 42) | ((uint64(v5)) << 41) | ((uint64(v5)) << 40) | ((uint64(v5)) << 39) | ((uint64(v5)) << 38) | ((uint64(v5)) << 37) | ((uint64(v5)) << 36) | ((uint64(v5)) << 35) | ((uint64(v5)) << 34) | ((uint64(v5)) << 33) | ((uint64(v5)) << 32) | (uint64(v3))))
	return uint64(v6)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_divuw_gpr_gpr_same_32__reg_a0__go__native_first(g0)
	_ = sink
}
