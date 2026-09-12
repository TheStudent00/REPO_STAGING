// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of add_gpr_gpr_16__flags__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(15, 0, v0), Extract(15, 0, v1))
package main

//go:noinline
func emu_add_gpr_gpr_16__flags__go(a uint16, b uint16) uint32 {
	return uint32((uint32(((uint32(uint32(a))) << 16) | (uint32(uint32(b))))))
}

var g0 uint16
var g1 uint16
var sink interface{}

func main() {
	sink = emu_add_gpr_gpr_16__flags__go(g0, g1)
	_ = sink
}
