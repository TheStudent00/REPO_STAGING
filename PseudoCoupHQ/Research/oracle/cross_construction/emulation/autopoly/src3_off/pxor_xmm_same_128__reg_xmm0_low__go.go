// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of pxor_xmm_same_128__reg_xmm0_low__go.
// The term's layer-5 text, LITERAL:
//   0
package main

import "math"

//go:noinline
func emu_pxor_xmm_same_128__reg_xmm0_low__go() float64 {
	return math.Float64frombits(uint64(uint64(0x0)))
}

var sink interface{}

func main() {
	sink = emu_pxor_xmm_same_128__reg_xmm0_low__go()
	_ = sink
}
