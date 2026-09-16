// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of srliw_gpr_gpr_imm_32__reg_a0__go__all_constructed.
//   Concat(0, Extract(31, 3, v0))
package main

//go:noinline
func emu_srliw_gpr_gpr_imm_32__reg_a0__go__all_constructed(a uint32) uint64 {
	var v0 uint32 = ((uint32((uint32(a)) >> 3)) & uint32(0x1fffffff))
	var v1 uint32 = v0
	var v2 uint64 = uint64(0x0)
	var v3 uint64 = (uint64(((uint64(v2)) << 29) | (uint64(v1))))
	return uint64(v3)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_srliw_gpr_gpr_imm_32__reg_a0__go__all_constructed(g0)
	_ = sink
}
