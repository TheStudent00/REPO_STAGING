// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of lui_gpr_imm_32__reg_a0__go.
// The term's layer-5 text, LITERAL:
//   12288
package main

//go:noinline
func emu_lui_gpr_imm_32__reg_a0__go() uint64 {
	return uint64(uint64(0x3000))
}

var sink interface{}

func main() {
	sink = emu_lui_gpr_imm_32__reg_a0__go()
	_ = sink
}
