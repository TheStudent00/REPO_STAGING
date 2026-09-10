// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of movss_mem_xmm_32__reg_xmm0__go.
// The term's layer-5 text, LITERAL:
//   Extract(31, 0, v0)
package main

import "math"

//go:noinline
func emu_movss_mem_xmm_32__reg_xmm0__go(a uint32) float32 {
	return math.Float32frombits(uint32(uint32(a)))
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_movss_mem_xmm_32__reg_xmm0__go(g0)
	_ = sink
}
