// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of divsd_xmm_xmm_64__reg_xmm0__go.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(Extract(63, 0, v0)) / fpToFP(Extract(63, 0, v1)))
package main

import "math"

//go:noinline
func emu_divsd_xmm_xmm_64__reg_xmm0__go(a float64, b float64) float64 {
	return math.Float64frombits(uint64(uint64(math.Float64bits(((a) / (b))))))
}

var g0 float64
var g1 float64
var sink interface{}

func main() {
	sink = emu_divsd_xmm_xmm_64__reg_xmm0__go(g0, g1)
	_ = sink
}
