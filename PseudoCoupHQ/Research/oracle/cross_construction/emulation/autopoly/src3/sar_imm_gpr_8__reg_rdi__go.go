// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of sar_imm_gpr_8__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(7, 0, v0) >> 3)
package main

//go:noinline
func emu_sar_imm_gpr_8__reg_rdi__go(a uint8) uint64 {
	return uint64((uint64(((uint64(uint64(0x0))) << 8) | (uint64(((uint32(uint32(((int32(uint32(a)) << 24) >> 24) >> ((uint32(uint32(0x3))) & uint32(0x7))))) & uint32(0xff)))))))
}

var g0 uint8
var sink interface{}

func main() {
	sink = emu_sar_imm_gpr_8__reg_rdi__go(g0)
	_ = sink
}
