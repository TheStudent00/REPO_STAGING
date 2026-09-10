// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of auipc_gpr_imm_32__reg_a0__go.
// The term's layer-5 text, LITERAL:
//   v0 + 12288
package main

//go:noinline
func emu_auipc_gpr_imm_32__reg_a0__go(a uint64) uint64 {
	return uint64((uint64((uint64(uint64(a))) + (uint64(uint64(0x3000))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_auipc_gpr_imm_32__reg_a0__go(g0)
	_ = sink
}
