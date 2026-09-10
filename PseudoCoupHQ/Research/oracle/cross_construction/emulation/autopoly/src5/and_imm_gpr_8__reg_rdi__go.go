// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of and_imm_gpr_8__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, ~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)))
package main

//go:noinline
func emu_and_imm_gpr_8__reg_rdi__go(a uint8, b uint8) uint64 {
	return uint64((uint64(((uint64(uint64(0x0))) << 8) | (uint64(((uint32(^(uint32(((uint32((uint32(((uint32(^(uint32(uint32(b))))) & uint32(0xff)))) | (uint32(((uint32(^(uint32(uint32(a))))) & uint32(0xff)))))) & uint32(0xff)))))) & uint32(0xff)))))))
}

var g0 uint8
var g1 uint8
var sink interface{}

func main() {
	sink = emu_and_imm_gpr_8__reg_rdi__go(g0, g1)
	_ = sink
}
