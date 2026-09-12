// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of addiw_gpr_gpr_imm_32__reg_a0__go__native_first.
//   Concat(Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v
package main

//go:noinline
func emu_addiw_gpr_gpr_imm_32__reg_a0__go__native_first(a uint32) uint64 {
	var v0 uint32 = uint32(a)
	var v1 uint32 = (uint32((uint32(v0)) + (uint32(uint32(0x3)))))
	var v2 uint32 = ((uint32((uint32(v1)) >> 31)) & uint32(0x1))
	var v3 uint64 = (uint64(((uint64(v2)) << 63) | ((uint64(v2)) << 62) | ((uint64(v2)) << 61) | ((uint64(v2)) << 60) | ((uint64(v2)) << 59) | ((uint64(v2)) << 58) | ((uint64(v2)) << 57) | ((uint64(v2)) << 56) | ((uint64(v2)) << 55) | ((uint64(v2)) << 54) | ((uint64(v2)) << 53) | ((uint64(v2)) << 52) | ((uint64(v2)) << 51) | ((uint64(v2)) << 50) | ((uint64(v2)) << 49) | ((uint64(v2)) << 48) | ((uint64(v2)) << 47) | ((uint64(v2)) << 46) | ((uint64(v2)) << 45) | ((uint64(v2)) << 44) | ((uint64(v2)) << 43) | ((uint64(v2)) << 42) | ((uint64(v2)) << 41) | ((uint64(v2)) << 40) | ((uint64(v2)) << 39) | ((uint64(v2)) << 38) | ((uint64(v2)) << 37) | ((uint64(v2)) << 36) | ((uint64(v2)) << 35) | ((uint64(v2)) << 34) | ((uint64(v2)) << 33) | ((uint64(v2)) << 32) | (uint64(v1))))
	return uint64(v3)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_addiw_gpr_gpr_imm_32__reg_a0__go__native_first(g0)
	_ = sink
}
