// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of lui_gpr_imm_32__reg_a0__go__native_first.
//   12288
package main

//go:noinline
func emu_lui_gpr_imm_32__reg_a0__go__native_first() uint64 {
	return uint64(uint64(0x3000))
}

var sink interface{}

func main() {
	sink = emu_lui_gpr_imm_32__reg_a0__go__native_first()
	_ = sink
}
