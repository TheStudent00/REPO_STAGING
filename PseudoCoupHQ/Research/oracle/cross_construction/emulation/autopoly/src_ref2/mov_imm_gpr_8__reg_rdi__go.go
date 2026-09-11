// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of mov_imm_gpr_8__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v0), Extract(7, 0, v1))
package main

//go:noinline
func emu_mov_imm_gpr_8__reg_rdi__go(a uint64, b uint8) uint64 {
	return uint64((uint64(((uint64(((uint64((uint64(a)) >> 8)) & uint64(0xffffffffffffff)))) << 8) | (uint64(uint32(b))))))
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_mov_imm_gpr_8__reg_rdi__go(g0, g1)
	_ = sink
}
