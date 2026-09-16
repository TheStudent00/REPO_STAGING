// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of auipc_gpr_imm_32__reg_a0__go__native_first.
//   v0 + 12288
package main

//go:noinline
func emu_auipc_gpr_imm_32__reg_a0__go__native_first(a uint64) uint64 {
	var v0 uint64 = (uint64((uint64(uint64(a))) + (uint64(uint64(0x3000)))))
	return uint64(v0)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_auipc_gpr_imm_32__reg_a0__go__native_first(g0)
	_ = sink
}
