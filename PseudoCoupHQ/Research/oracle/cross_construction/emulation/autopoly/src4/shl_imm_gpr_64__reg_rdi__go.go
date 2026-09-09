// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of shl_imm_gpr_64__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(60, 0, v0), 0)
package main

//go:noinline
func emu_shl_imm_gpr_64__reg_rdi__go(a uint64) uint64 {
	return uint64((uint64(((uint64(((uint64((uint64(a)) >> 0)) & uint64(0x1fffffffffffffff)))) << 3) | (uint64(uint32(0x0))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_shl_imm_gpr_64__reg_rdi__go(g0)
	_ = sink
}
