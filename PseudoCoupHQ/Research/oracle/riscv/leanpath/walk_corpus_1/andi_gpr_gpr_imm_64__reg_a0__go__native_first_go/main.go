// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of andi_gpr_gpr_imm_64__reg_a0__go__native_first.
//   Concat(0, Extract(1, 0, v0))
package main

//go:noinline
func emu_andi_gpr_gpr_imm_64__reg_a0__go__native_first(a uint8) uint64 {
	var v0 uint32 = ((uint32((uint32(a)) >> 0)) & uint32(0x3))
	var v1 uint64 = (uint64(((uint64(uint64(0x0))) << 2) | (uint64(v0))))
	return uint64(v1)
}

var g0 uint8
var sink interface{}

func main() {
	sink = emu_andi_gpr_gpr_imm_64__reg_a0__go__native_first(g0)
	_ = sink
}
