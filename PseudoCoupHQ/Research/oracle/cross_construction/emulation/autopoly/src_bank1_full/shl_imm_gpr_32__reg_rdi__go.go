// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of shl_imm_gpr_32__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(28, 0, v0), 0)
package main

//go:noinline
func emu_shl_imm_gpr_32__reg_rdi__go(a uint32) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | ((uint64(((uint32((uint32(a)) >> 0)) & uint32(0x1fffffff)))) << 3) | (uint64(uint32(0x0))))))
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_shl_imm_gpr_32__reg_rdi__go(g0)
	_ = sink
}
