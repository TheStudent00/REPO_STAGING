// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of sar_imm_gpr_64__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   v0 >> 3
package main

//go:noinline
func emu_sar_imm_gpr_64__reg_rdi__go(a uint64) uint64 {
	return uint64((uint64(uint64((int64(uint64(a))) >> ((uint64(uint64(0x3))) & uint64(0x3f))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_sar_imm_gpr_64__reg_rdi__go(g0)
	_ = sink
}
