// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cmovl_gpr_gpr_64__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   v0
package main

//go:noinline
func emu_cmovl_gpr_gpr_64__reg_rdi__go(a uint64, b uint64, c uint64) uint64 {
	return uint64(uint64(c))
}

var g0 uint64
var g1 uint64
var g2 uint64
var sink interface{}

func main() {
	sink = emu_cmovl_gpr_gpr_64__reg_rdi__go(g0, g1, g2)
	_ = sink
}
