// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of unpckhpd_xmm_xmm_128__reg_xmm0_low__go.
// The term's layer-5 text, LITERAL:
//   v0
package main

import "math"

//go:noinline
func emu_unpckhpd_xmm_xmm_128__reg_xmm0_low__go(a uint64) float64 {
	return math.Float64frombits(uint64(uint64(a)))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_unpckhpd_xmm_xmm_128__reg_xmm0_low__go(g0)
	_ = sink
}
