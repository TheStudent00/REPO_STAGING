// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of mov_imm_gpr_64__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   3
package main

//go:noinline
func emu_mov_imm_gpr_64__reg_rdi__go() uint64 {
	return uint64(uint64(0x3))
}

var sink interface{}

func main() {
	sink = emu_mov_imm_gpr_64__reg_rdi__go()
	_ = sink
}
