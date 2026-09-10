// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of test_gpr_same_16__flags__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(15, 0, v0), 0)
package main

//go:noinline
func emu_test_gpr_same_16__flags__go(a uint16) uint32 {
	return uint32((uint32(((uint32(uint32(a))) << 16) | (uint32(uint32(0x0))))))
}

var g0 uint16
var sink interface{}

func main() {
	sink = emu_test_gpr_same_16__flags__go(g0)
	_ = sink
}
