// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of xori_gpr_gpr_imm_64__reg_a0__go__all_constructed.
//   Concat(Extract(63, 2, v0), ~Extract(1, 0, v0))
package main

//go:noinline
func emu_xori_gpr_gpr_imm_64__reg_a0__go__all_constructed(a uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x3))
	var v1 uint32 = ((uint32(^(uint32(v0)))) & uint32(0x3))
	var v2 uint64 = ((uint64((uint64(a)) >> 2)) & uint64(0x3fffffffffffffff))
	var v3 uint32 = v1
	var v4 uint64 = v2
	var v5 uint64 = (uint64(((uint64(v4)) << 2) | (uint64(v3))))
	return uint64(v5)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_xori_gpr_gpr_imm_64__reg_a0__go__all_constructed(g0)
	_ = sink
}
