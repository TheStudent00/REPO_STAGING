// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of subsd_mem_xmm_64__reg_xmm0__go.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(-fpToFP(v0) + fpToFP(Extract(63, 0, v1)))
package main

import "math"

//go:noinline
func emu_subsd_mem_xmm_64__reg_xmm0__go(a uint64, b float64) float64 {
	return math.Float64frombits(uint64(uint64(math.Float64bits((((-(math.Float64frombits(uint64(uint64(a)))))) + (b))))))
}

var g0 uint64
var g1 float64
var sink interface{}

func main() {
	sink = emu_subsd_mem_xmm_64__reg_xmm0__go(g0, g1)
	_ = sink
}
