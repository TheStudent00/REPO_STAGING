// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of movzbl_widen_mem_gpr_32__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(7, 0, v0))
package main

//go:noinline
func emu_movzbl_widen_mem_gpr_32__reg_rdi__go(a uint8) uint64 {
	return uint64((uint64(((uint64(uint64(0x0))) << 8) | (uint64(uint32(a))))))
}

var g0 uint8
var sink interface{}

func main() {
	sink = emu_movzbl_widen_mem_gpr_32__reg_rdi__go(g0)
	_ = sink
}
