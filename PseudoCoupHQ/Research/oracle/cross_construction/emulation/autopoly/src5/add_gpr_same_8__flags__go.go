// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of add_gpr_same_8__flags__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(7, 0, v0), Extract(7, 0, v0))
package main

//go:noinline
func emu_add_gpr_same_8__flags__go(a uint8) uint16 {
	return uint16(((uint32(((uint32(uint32(a))) << 8) | (uint32(uint32(a))))) & uint32(0xffff)))
}

var g0 uint8
var sink interface{}

func main() {
	sink = emu_add_gpr_same_8__flags__go(g0)
	_ = sink
}
