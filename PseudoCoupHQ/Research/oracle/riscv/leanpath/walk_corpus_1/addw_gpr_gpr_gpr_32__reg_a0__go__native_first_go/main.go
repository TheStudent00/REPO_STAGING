// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of addw_gpr_gpr_gpr_32__reg_a0__go__native_first.
//   Concat(Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract(31, 0, v0) + Extract(31, 0, v1)), Extract(31, 31, Extract
package main

//go:noinline
func emu_addw_gpr_gpr_gpr_32__reg_a0__go__native_first(a uint32, b uint32) uint64 {
	var v0 uint32 = uint32(b)
	var v1 uint32 = uint32(a)
	var v2 uint32 = (uint32((uint32(v1)) + (uint32(v0))))
	var v3 uint32 = ((uint32((uint32(v2)) >> 31)) & uint32(0x1))
	var v4 uint64 = (uint64(((uint64(v3)) << 63) | ((uint64(v3)) << 62) | ((uint64(v3)) << 61) | ((uint64(v3)) << 60) | ((uint64(v3)) << 59) | ((uint64(v3)) << 58) | ((uint64(v3)) << 57) | ((uint64(v3)) << 56) | ((uint64(v3)) << 55) | ((uint64(v3)) << 54) | ((uint64(v3)) << 53) | ((uint64(v3)) << 52) | ((uint64(v3)) << 51) | ((uint64(v3)) << 50) | ((uint64(v3)) << 49) | ((uint64(v3)) << 48) | ((uint64(v3)) << 47) | ((uint64(v3)) << 46) | ((uint64(v3)) << 45) | ((uint64(v3)) << 44) | ((uint64(v3)) << 43) | ((uint64(v3)) << 42) | ((uint64(v3)) << 41) | ((uint64(v3)) << 40) | ((uint64(v3)) << 39) | ((uint64(v3)) << 38) | ((uint64(v3)) << 37) | ((uint64(v3)) << 36) | ((uint64(v3)) << 35) | ((uint64(v3)) << 34) | ((uint64(v3)) << 33) | ((uint64(v3)) << 32) | (uint64(v2))))
	return uint64(v4)
}

var g0 uint32
var g1 uint32
var sink interface{}

func main() {
	sink = emu_addw_gpr_gpr_gpr_32__reg_a0__go__native_first(g0, g1)
	_ = sink
}
