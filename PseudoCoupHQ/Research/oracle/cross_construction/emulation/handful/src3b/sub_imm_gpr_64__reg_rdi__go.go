// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of sub_imm_gpr_64__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   v0 + 18446744073709551613
package main

//go:noinline
func emu_sub_imm_gpr_64__reg_rdi__go(a uint64) uint64 {
	return uint64((uint64((uint64(uint64(a))) + (uint64(uint64(0xfffffffffffffffd))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_sub_imm_gpr_64__reg_rdi__go(g0)
	_ = sink
}
