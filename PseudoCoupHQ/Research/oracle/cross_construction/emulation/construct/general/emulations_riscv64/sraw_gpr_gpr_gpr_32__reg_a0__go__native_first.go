// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sraw_gpr_gpr_gpr_32__reg_a0__go__native_first.
//   Concat(Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))), Extract(31, 31, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1)
package main

//go:noinline
func emu_sraw_gpr_gpr_gpr_32__reg_a0__go__native_first(a uint32, b uint8) uint64 {
	var v0 uint32 = ((uint32((uint32(b)) >> 0)) & uint32(0x1f))
	var v1 uint32 = (uint32(((uint32(uint32(0x0))) << 5) | (uint32(v0))))
	var v2 uint32 = uint32(a)
	var v3 uint32 = (uint32(uint32((int32(v2)) >> ((uint32(v1)) & uint32(0x1f)))))
	var v4 uint32 = ((uint32((uint32(v3)) >> 31)) & uint32(0x1))
	var v5 uint64 = (uint64(((uint64(v4)) << 63) | ((uint64(v4)) << 62) | ((uint64(v4)) << 61) | ((uint64(v4)) << 60) | ((uint64(v4)) << 59) | ((uint64(v4)) << 58) | ((uint64(v4)) << 57) | ((uint64(v4)) << 56) | ((uint64(v4)) << 55) | ((uint64(v4)) << 54) | ((uint64(v4)) << 53) | ((uint64(v4)) << 52) | ((uint64(v4)) << 51) | ((uint64(v4)) << 50) | ((uint64(v4)) << 49) | ((uint64(v4)) << 48) | ((uint64(v4)) << 47) | ((uint64(v4)) << 46) | ((uint64(v4)) << 45) | ((uint64(v4)) << 44) | ((uint64(v4)) << 43) | ((uint64(v4)) << 42) | ((uint64(v4)) << 41) | ((uint64(v4)) << 40) | ((uint64(v4)) << 39) | ((uint64(v4)) << 38) | ((uint64(v4)) << 37) | ((uint64(v4)) << 36) | ((uint64(v4)) << 35) | ((uint64(v4)) << 34) | ((uint64(v4)) << 33) | ((uint64(v4)) << 32) | (uint64(v3))))
	return uint64(v5)
}

var g0 uint32
var g1 uint8
var sink interface{}

func main() {
	sink = emu_sraw_gpr_gpr_gpr_32__reg_a0__go__native_first(g0, g1)
	_ = sink
}
