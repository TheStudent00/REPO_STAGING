// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of remuw_gpr_gpr_gpr_32__reg_a0__go__native_first.
//   Concat(If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v1), Extract(31, 31, bvurem_i(
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_remuw_gpr_gpr_gpr_32__reg_a0__go__native_first(a uint32, b uint32) uint64 {
	var v0 uint32 = uint32(a)
	var v1 uint32 = uint32(b)
	var v2 uint32 = (uint32((uint32(v1)) % (uint32(v0))))
	var v3 bool = ((uint32(v0)) == (uint32(uint32(0x0))))
	var v4 uint32 = sel32(v3, uint32(v1), uint32(v2))
	var v5 uint32 = ((uint32((uint32(v2)) >> 31)) & uint32(0x1))
	var v6 uint32 = ((uint32((uint32(b)) >> 31)) & uint32(0x1))
	var v7 uint32 = sel32(v3, uint32(v6), uint32(v5))
	var v8 uint64 = (uint64(((uint64(v7)) << 63) | ((uint64(v7)) << 62) | ((uint64(v7)) << 61) | ((uint64(v7)) << 60) | ((uint64(v7)) << 59) | ((uint64(v7)) << 58) | ((uint64(v7)) << 57) | ((uint64(v7)) << 56) | ((uint64(v7)) << 55) | ((uint64(v7)) << 54) | ((uint64(v7)) << 53) | ((uint64(v7)) << 52) | ((uint64(v7)) << 51) | ((uint64(v7)) << 50) | ((uint64(v7)) << 49) | ((uint64(v7)) << 48) | ((uint64(v7)) << 47) | ((uint64(v7)) << 46) | ((uint64(v7)) << 45) | ((uint64(v7)) << 44) | ((uint64(v7)) << 43) | ((uint64(v7)) << 42) | ((uint64(v7)) << 41) | ((uint64(v7)) << 40) | ((uint64(v7)) << 39) | ((uint64(v7)) << 38) | ((uint64(v7)) << 37) | ((uint64(v7)) << 36) | ((uint64(v7)) << 35) | ((uint64(v7)) << 34) | ((uint64(v7)) << 33) | ((uint64(v7)) << 32) | (uint64(v4))))
	return uint64(v8)
}

var g0 uint32
var g1 uint32
var sink interface{}

func main() {
	sink = emu_remuw_gpr_gpr_gpr_32__reg_a0__go__native_first(g0, g1)
	_ = sink
}
