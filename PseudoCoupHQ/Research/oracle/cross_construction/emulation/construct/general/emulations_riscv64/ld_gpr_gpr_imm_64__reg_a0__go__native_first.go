// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ld_gpr_gpr_imm_64__reg_a0__go__native_first.
//   v0
package main

//go:noinline
func emu_ld_gpr_gpr_imm_64__reg_a0__go__native_first(a uint64) uint64 {
	return uint64(uint64(a))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_ld_gpr_gpr_imm_64__reg_a0__go__native_first(g0)
	_ = sink
}
