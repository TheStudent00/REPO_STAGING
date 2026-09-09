// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of shr_imm_gpr_32__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 3, v0))
package main

//go:noinline
func emu_shr_imm_gpr_32__reg_rdi__go(a uint32) uint64 {
	return uint64((uint64(((uint64(uint64(0x0))) << 29) | (uint64(((uint32((uint32(a)) >> 3)) & uint32(0x1fffffff)))))))
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_shr_imm_gpr_32__reg_rdi__go(g0)
	_ = sink
}
