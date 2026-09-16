// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of xori_gpr_gpr_imm_64__reg_a0__go__native_first.
//   Concat(Extract(63, 2, v0), ~Extract(1, 0, v0))
package main

//go:noinline
func emu_xori_gpr_gpr_imm_64__reg_a0__go__native_first(a uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x3))
	var v1 uint32 = ((uint32(^(uint32(v0)))) & uint32(0x3))
	var v2 uint64 = ((uint64((uint64(a)) >> 2)) & uint64(0x3fffffffffffffff))
	var v3 uint64 = (uint64(((uint64(v2)) << 2) | (uint64(v1))))
	return uint64(v3)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_xori_gpr_gpr_imm_64__reg_a0__go__native_first(g0)
	_ = sink
}
