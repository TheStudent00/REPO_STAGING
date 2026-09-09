// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of or_imm_gpr_8__flags__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(7, 2, v0), 768)
package main

//go:noinline
func emu_or_imm_gpr_8__flags__go(a uint8) uint16 {
	return uint16(((uint32(((uint32(((uint32((uint32(a)) >> 2)) & uint32(0x3f)))) << 10) | (uint32(uint32(0x300))))) & uint32(0xffff)))
}

var g0 uint8
var sink interface{}

func main() {
	sink = emu_or_imm_gpr_8__flags__go(g0)
	_ = sink
}
