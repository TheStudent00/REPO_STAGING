// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of mov_imm_gpr_32__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0))
package main

//go:noinline
func emu_mov_imm_gpr_32__reg_rdi__go(a uint32) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64(uint32(a))))))
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_mov_imm_gpr_32__reg_rdi__go(g0)
	_ = sink
}
