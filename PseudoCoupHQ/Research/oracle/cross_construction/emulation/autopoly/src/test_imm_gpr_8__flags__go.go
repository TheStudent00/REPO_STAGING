// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of test_imm_gpr_8__flags__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(1, 0, v0), 0)
package main

//go:noinline
func emu_test_imm_gpr_8__flags__go(a uint8) uint16 {
	return uint16(((uint32(((uint32(uint32(0x0))) << 10) | ((uint32(((uint32((uint32(a)) >> 0)) & uint32(0x3)))) << 8) | (uint32(uint32(0x0))))) & uint32(0xffff)))
}

var g0 uint8
var sink interface{}

func main() {
	sink = emu_test_imm_gpr_8__flags__go(g0)
	_ = sink
}
