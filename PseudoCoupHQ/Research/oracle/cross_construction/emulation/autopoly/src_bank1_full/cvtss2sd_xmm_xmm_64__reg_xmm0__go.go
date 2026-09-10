// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cvtss2sd_xmm_xmm_64__reg_xmm0__go.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(RNE(), fpToFP(Extract(31, 0, v0))))
package main

import "math"

//go:noinline
func emu_cvtss2sd_xmm_xmm_64__reg_xmm0__go(a float32) float64 {
	return math.Float64frombits(uint64(uint64(math.Float64bits(float64(a)))))
}

var g0 float32
var sink interface{}

func main() {
	sink = emu_cvtss2sd_xmm_xmm_64__reg_xmm0__go(g0)
	_ = sink
}
