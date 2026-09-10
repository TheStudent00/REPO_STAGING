// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of jalr_gpr_imm_64__reg_a0__go.
// The term's layer-5 text, LITERAL:
//   v0 + 4
package main

//go:noinline
func emu_jalr_gpr_imm_64__reg_a0__go(a uint64) uint64 {
	return uint64((uint64((uint64(uint64(a))) + (uint64(uint64(0x4))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_jalr_gpr_imm_64__reg_a0__go(g0)
	_ = sink
}
