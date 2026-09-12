// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of test_imm_gpr_8__flags__go.
// The term's layer-5 text, LITERAL:
//   Concat(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)), 0)
package main

//go:noinline
func emu_test_imm_gpr_8__flags__go(a uint8, b uint8) uint16 {
	return uint16(((uint32(((uint32(((uint32(^(uint32(((uint32((uint32(((uint32(^(uint32(uint32(b))))) & uint32(0xff)))) | (uint32(((uint32(^(uint32(uint32(a))))) & uint32(0xff)))))) & uint32(0xff)))))) & uint32(0xff)))) << 8) | (uint32(uint32(0x0))))) & uint32(0xffff)))
}

var g0 uint8
var g1 uint8
var sink interface{}

func main() {
	sink = emu_test_imm_gpr_8__flags__go(g0, g1)
	_ = sink
}
