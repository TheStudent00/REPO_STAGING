// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of idiv_gpr_one_32__reg_rax__go__native_first.
//   Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
package main

//go:noinline
func emu_idiv_gpr_one_32__reg_rax__go__native_first(a uint32, b uint32, c uint32) uint64 {
	var v0 uint32 = uint32(c)
	var v1 uint32 = ((uint32((uint32(c)) >> 31)) & uint32(0x1))
	var v2 uint64 = (uint64(((uint64(v1)) << 63) | ((uint64(v1)) << 62) | ((uint64(v1)) << 61) | ((uint64(v1)) << 60) | ((uint64(v1)) << 59) | ((uint64(v1)) << 58) | ((uint64(v1)) << 57) | ((uint64(v1)) << 56) | ((uint64(v1)) << 55) | ((uint64(v1)) << 54) | ((uint64(v1)) << 53) | ((uint64(v1)) << 52) | ((uint64(v1)) << 51) | ((uint64(v1)) << 50) | ((uint64(v1)) << 49) | ((uint64(v1)) << 48) | ((uint64(v1)) << 47) | ((uint64(v1)) << 46) | ((uint64(v1)) << 45) | ((uint64(v1)) << 44) | ((uint64(v1)) << 43) | ((uint64(v1)) << 42) | ((uint64(v1)) << 41) | ((uint64(v1)) << 40) | ((uint64(v1)) << 39) | ((uint64(v1)) << 38) | ((uint64(v1)) << 37) | ((uint64(v1)) << 36) | ((uint64(v1)) << 35) | ((uint64(v1)) << 34) | ((uint64(v1)) << 33) | ((uint64(v1)) << 32) | (uint64(v0))))
	var v3 uint32 = uint32(b)
	var v4 uint32 = uint32(a)
	var v5 uint64 = (uint64(((uint64(v4)) << 32) | (uint64(v3))))
	var v6 uint64 = (uint64(uint64((int64(v5)) / (int64(v2)))))
	var v7 uint32 = (uint32((uint64(v6)) >> 0))
	var v8 uint64 = (uint64(((uint64(uint32(0x0))) << 32) | (uint64(v7))))
	return uint64(v8)
}

var g0 uint32
var g1 uint32
var g2 uint32
var sink interface{}

func main() {
	sink = emu_idiv_gpr_one_32__reg_rax__go__native_first(g0, g1, g2)
	_ = sink
}
