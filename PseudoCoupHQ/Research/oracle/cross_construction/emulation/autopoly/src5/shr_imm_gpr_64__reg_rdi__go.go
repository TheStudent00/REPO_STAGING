// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of shr_imm_gpr_64__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(63, 3, v0))
package main

//go:noinline
func emu_shr_imm_gpr_64__reg_rdi__go(a uint64) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 61) | (uint64(((uint64((uint64(a)) >> 3)) & uint64(0x1fffffffffffffff)))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_shr_imm_gpr_64__reg_rdi__go(g0)
	_ = sink
}
